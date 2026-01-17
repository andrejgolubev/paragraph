import { useState, useEffect, useCallback, useRef } from "react"
import HomeworkModal from "../HomeworkModal" 
import paperclip from "../../../images/homework/paperclip.svg"
import paperclipDark from "../../../images/homework/paperclip-dark.svg"
import homeworkAPI from "../../../api/homeworkAPI"
import { Mosaic } from "react-loading-indicators"
import { getDateValueFromDisplay} from "../../../utils/converters"
import { useWindowSize } from "../../../hooks/useWindowSize"
import MobileItem from "./mobile/MobileItem"
import Button from "./mobile/Button"
import { useDropdownStore } from "../../../store/dropdownStore"
import { useThemeStore } from "../../../store/themeStore"



const ScheduleContainer = () => {
  const darkTheme = useThemeStore(state => state.darkTheme)

  const { groupDataValue, dateDataValue } = useDropdownStore()
  const [scheduleData, setScheduleData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showDialog, setShowDialog] = useState(false)
  const [homeworkText, setHomeworkText] = useState("")
  const [homeworkUpdated, setHomeworkUpdated] = useState("")
  const [homeworkAuthor, setHomeworkAuthor] = useState('')
  const [year, setYear] = useState(new Date().getFullYear())
  const [currentLessonInfo, setCurrentLessonInfo] = useState({})
  const [mobileLesson, setMobileLesson] = useState(0)
  const windowSize = useWindowSize()
  const [debouncedWidth, setDebouncedWidth] = useState(windowSize.width)
  const widthDebounceRef = useRef(null)
  const isMobile = debouncedWidth < 1001

  useEffect(() => {
    if (widthDebounceRef.current) {
      clearTimeout(widthDebounceRef.current)
    }
    widthDebounceRef.current = setTimeout(() => {
      setDebouncedWidth(windowSize.width)
    }, 30)
    console.log('debouncedWidth :>>', debouncedWidth);
    return () => {
      if (widthDebounceRef.current) {
        clearTimeout(widthDebounceRef.current)
      }
    }
  }, [windowSize.width])



  useEffect(() => {
    // setGroupDataValueCookies('groupDataValue', groupDataValue, {maxAge: 60*60*24*14}) // чтобы сразу загружалась нужная группа 
    // setDateDataValueCookies('dateDataValue', dateDataValue, {maxAge: 60*60*24*14}) // чтобы сразу загружалась нужная дата

    console.log("ScheduleContainer - текущие значения:", {
      groupDataValue,
      dateDataValue,
    })

  }, [groupDataValue, dateDataValue])

  useEffect( () => {
    if (dateDataValue) {
      setYear(dateDataValue.slice(0, 4))
    }
  }, [dateDataValue])

  const scheduleDateDataValue = getDateValueFromDisplay(
    scheduleData?.days?.[0]?.date || "" , 
    year
  )
  
  
  // ДЛЯ ИСПОЛЬЗОВАНИЯ как dateDataValue для сохранения конкретной домашки, т.к. домашка прикрепляется к неделе,
  // а не к конкретной дате т.е. 2025-12-22, 2025-12-29, 2026-01-05 и т.д.

  // Загрузка расписания
  const loadSchedule = useCallback(async () => {
    // try {
      setLoading(true)
      
      homeworkAPI.getScheduleData({groupDataValue, dateDataValue}).then((data) => {
        setScheduleData(data)
        setError(null)
      }).catch((err) => {
        console.error("Error loading schedule:", err)
        setError(err.message)
      }).finally(() => {
        setLoading(false)
      })
   
  }, [groupDataValue, dateDataValue])

  // загружаем расписание при монтировании расписания
  useEffect(() => {
    loadSchedule()
  }, [loadSchedule])

  // Обработчик клика по домашке
  const handleHomeworkClick = (lessInfo) => {
    const {
      groupDataValue,
      lessonIndex,
      lessonDate,
      lessonName,
    } = lessInfo

    homeworkAPI
      .loadHomeworkData(groupDataValue, scheduleDateDataValue, lessonIndex)
      .then((resp) => {
        const { homework, updated, username } = resp
        setHomeworkUpdated(updated)
        setHomeworkText(homework)
        setHomeworkAuthor(username)
      }).catch( (err) => {
        console.log('err from ScheduleCont :>> ', err);
      }
      )

    const lessonInfo = {
      groupDataValue,
      lessonIndex: parseInt(lessonIndex),
      lessonDate,
      lessonName,
    }

    setCurrentLessonInfo( 
      { ...lessonInfo, dateDataValue: scheduleDateDataValue } 
    )
    
    setShowDialog(true)
  }

  // Функция для подсветки текущего дня
  const getDayClass = (dayName, dateText) => {
    const weekDaysMap = {
      Понедельник: 1,
      Вторник: 2,
      Среда: 3,
      Четверг: 4,
      Пятница: 5,
      Суббота: 6,
    }

    const currentDate = new Date()
    const currentWeekDay = currentDate.getDay()
    const currentDayOfMonth = currentDate.getDate()

    // В JavaScript getDay() возвращает 0 для воскресенья, 1 для понедельника и т.д.
    const adjustedWeekDay = currentWeekDay === 0 ? 7 : currentWeekDay

    const isCurrentWeekday = weekDaysMap[dayName] === adjustedWeekDay
    const isCurrentDate = parseInt(dateText) === currentDayOfMonth

    return isCurrentWeekday && isCurrentDate ? "active-day" : ""
  }

  

  // Форматирование текста занятия
  const formatLessonText = (lesson) => {
    const lessonName = lesson.text.split(", ")[0]
    const lessonRest = lesson.text.replace(
      lesson.text.includes(", ") ? lessonName + ", " : lessonName,
      ""
    )

    const parts = lessonRest.split(",").filter((part) => part.trim() !== "")

    return (
      <>
        <strong>{lessonName}</strong>
        {parts.map((part, index) => (
          <p key={index}>
            {part.trim()}
            {index < parts.length - 1 ? "," : ""}
          </p>
        ))}
      </>
    )
  }

  const lessonIndexRef = useRef(1)
  // Рендер расписания
  const renderDesktopSchedule = (scheduleData) => {
    if (!scheduleData) return null

    const datesArr = scheduleData.days.map((day) => day.date)
    
    lessonIndexRef.current = 1

    return (
      <table
        className={`table ${darkTheme ? " dark" : ""}`}
        id="schedule-container"
      >
        <thead>
          <tr className="table_row_high">
            <th>время</th>
            {scheduleData.days.map((day, index) => (
              <th key={index} className={getDayClass(day.day, day.date)}>
                <p id="week-date">{day.date}</p>
                <p id="week-day">{day.day}</p>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {scheduleData.schedule.map((timeSlot, timeIndex) => (
            <tr key={timeIndex}>
              <td>
                <p>{timeSlot.time_start}</p>
                <p>{timeSlot.time_end}</p>
              </td>
              {timeSlot.lessons.map((dayLessons, dayIndex) => {
                const dataDate = datesArr[dayIndex]
                const currentLessonIndex = lessonIndexRef.current++

                return (
                  <td
                    key={`${timeIndex}-${dayIndex}`}
                    data-date={dataDate}
                  >
                    {dayLessons.length > 0 ? (
                      dayLessons.map((
                        lesson, 
                        lessonIndex
                      ) => {
                        const lessonId =
                          lesson.type === "Лек."
                            ? "lec"
                            : lesson.type === "Упр."
                            ? "upr"
                            : lesson.type === "Лаб."
                            ? "lab"
                            : lesson.type === "Конс."
                            ? "consult"
                            : lesson.type === "Экзамен"
                            ? "exam"
                            : lesson.type === "Зач."
                            ? "cred"
                            : "default"

                        const lessonInfo = {
                          groupDataValue: groupDataValue,
                          dateDataValue: getDateValueFromDisplay(
                            datesArr[dayIndex]
                          ),
                          lessonIndex: currentLessonIndex,
                          lessonName: lesson.text.split(", ").slice(0, 2).join(", "),
                          lessonDate: dataDate,
                        }

                        return (
                          <div
                            key={lessonIndex}
                            className="lesson-item"
                            id={lessonId}
                          >
                            {lesson.type && (
                              <span
                                className={`lesson-type ${lessonId}`}
                              >
                                {lesson.type}
                              </span>
                            )}
                            <div
                              className="homework"
                              onClick={() => {
                                handleHomeworkClick(lessonInfo)
                              }}
                              style={{ cursor: "pointer" }}
                              title="добавить д/з"
                            >
                              <img 
                                src={darkTheme? paperclipDark : paperclip} 
                                alt="Homework" 
                              />
                            </div>
                            <div className="lesson-text">
                              {formatLessonText(lesson)}
                            </div>
                          </div>
                        )
                      })
                    ) : (
                      <div className="lesson-empty"></div>
                    )}
                  </td>
                )
              })}
            </tr>
          ))}
        </tbody>
      </table>
    )
  }

  

  const renderMobileSchedule = (scheduleData) => {
    if (!scheduleData) return null 

    console.log('scheduleData :>> ', scheduleData);

    const weekdays = ["Пн","Вт","Ср","Чт","Пт","Сб"]
    const daysArr = weekdays.map((day, dayIndex) => (
      {day,
      lessons: scheduleData.schedule.map(({lessons, time_start, time_end}, slotIndex) => ({
        lesson: lessons[dayIndex],
        lessonId: slotIndex*6 + dayIndex + 1, 
        start: time_start, 
        end: time_end,
      }))}
    ))

    const renderMobileItem = (weekDayIndex) => {
      const datesArr = scheduleData.days.map((day) => day.date)

      const mobileItem = daysArr[weekDayIndex].lessons.map(({lesson, lessonId, start, end }) => (
      <MobileItem 
        time={`${start}-${end}`} 
        texts={lesson?.map(sublesson => (sublesson.text))} 
        types={lesson?.map(sublesson => (sublesson.type))}  
        lessonId={lessonId}

        onClick={() => handleHomeworkClick({
          groupDataValue: groupDataValue,
          dateDataValue: scheduleDateDataValue,
          lessonIndex: lessonId,
          lessonName: lesson?.map(sublesson => (sublesson.text)).slice(0, 2).join(", "),
          lessonDate: datesArr[weekDayIndex],
        })}

      />
      )) 

      if (mobileItem.every((item) => item.props?.texts.length === 0)) { 
        return (
          <p className="mobile-schedule__content__item__no-lessons-text">в этот день нет занятий</p>
        )
      }
      return mobileItem
    }



    return (
      <div className="mobile-schedule">
        <div className="mobile-schedule__header">
          {weekdays.map((weekday, index) => (
            <Button
              isActive={index === mobileLesson}
              onClick={() => setMobileLesson(index)}
            >
              {weekday}
            </Button>
          ))}
        </div>
        <div className="mobile-schedule__content">
          {renderMobileItem(mobileLesson)}
        </div>
      </div>
    )
  }

  // Состояния загрузки и ошибки
  if (loading) {
    if (!isMobile) { 
    return (
      <>
        <div className="schedule-container loading"></div>
        <div className={`loading-indicator`}>
          <Mosaic
            color={darkTheme? '#d2d2d2' : '#fff'}
            
            size="large"
            text="загрузка..."
            textColor="#CBCBDE"
          />
        </div>
      </>
    )} else {
      return (
        <>
        <div className="mobile-schedule loading">
          <div className="mobile-schedule__header">
            <button className="mobile-schedule__header__button">
              Пн
            </button>
            <button className="mobile-schedule__header__button">
              Вт
            </button>
            <button className="mobile-schedule__header__button">
              Ср
            </button>
            <button className="mobile-schedule__header__button">
              Чт
            </button>
            <button className="mobile-schedule__header__button">
              Пт
            </button>
            <button className="mobile-schedule__header__button">
              Сб
            </button>
          </div>
          <div className="mobile-schedule__loading-wrap">
            <div className="loading-indicator mobile">
              <Mosaic
                color={'#E6E6E6'}
                size="large"
                text="загрузка..."
                textColor="#D0D0D0"
              />
            </div>
          </div>
        </div>
      </>
      )
    }
  }

  if (error) {
    return ( 
      <div className='schedule-container error'>
        <button className={`${darkTheme ? " dark" : ""}`}
        onClick={loadSchedule}>
          <p>{error}</p>
          <p>нажмите сюда, чтобы повторить </p>
          <p>попытку</p>
        </button>
      </div>
    )
  }

  return (
    <>
      <div
        className={`
          ${ isMobile ? "mobile-schedule" : "schedule-container" } 
          ${ scheduleData ? "loaded" : "loading" }`
        }
      >
        {isMobile ? renderMobileSchedule(scheduleData) : renderDesktopSchedule(scheduleData)}
      </div>

      {showDialog && (
        <HomeworkModal
          lessonInfo={currentLessonInfo}
          homeworkText={homeworkText}
          homeworkUpdated={homeworkUpdated}
          showDialog={showDialog}
          setShowDialog={setShowDialog}
          homeworkAuthor={homeworkAuthor}
        />
      )}
    </>
  )
}

export default ScheduleContainer
