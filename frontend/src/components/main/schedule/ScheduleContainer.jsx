import { useState, useEffect, useCallback, useRef } from "react"
import HomeworkModal from "../HomeworkModal" 
import paperclip from "../../../images/homework/paperclip.svg"
import paperclipDark from "../../../images/homework/paperclip-dark.svg"
import API, { showNotificationOuter } from "../../../api/API"
import { Mosaic } from "react-loading-indicators"
import { getDateValueFromDisplay} from "../../../utils/converters"
import { useWindowSize } from "../../../hooks/useWindowSize"
import MobileItem from "./mobile/MobileItem"
import Button from "./mobile/Button"
import { useDropdownStore } from "../../../store/dropdownStore"
import { useThemeStore } from "../../../store/themeStore"


const ScheduleContainer = () => {
  const {darkTheme, notesEnabled} = useThemeStore()
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
  const [mobileLesson, setMobileLesson] = useState((new Date().getDay()-1)%6)
  const windowSize = useWindowSize()
  const [debouncedWidth, setDebouncedWidth] = useState(windowSize.width)
  const widthDebounceRef = useRef(null)
  const isMobile = debouncedWidth < 1001

  const [homeworkExistsMap, setHomeworkExistsMap] = useState({})

  useEffect(() => {
    if (widthDebounceRef.current) {
      clearTimeout(widthDebounceRef.current)
    }
    widthDebounceRef.current = setTimeout(() => {
      setDebouncedWidth(windowSize.width)
    }, 30)
    return () => {
      if (widthDebounceRef.current) {
        clearTimeout(widthDebounceRef.current)
      }
    }
  }, [windowSize.width])


  useEffect( () => {
    if (dateDataValue) {
      setYear(dateDataValue.slice(0, 4))
    }
  }, [dateDataValue])

  
  const scheduleDateDataValue = getDateValueFromDisplay(
    scheduleData?.days?.[0]?.date || "" , 
    year
  )
 

  // Загрузка расписания
  const loadSchedule = useCallback(async () => {
    setLoading(true)
    
    API.getScheduleData({groupDataValue, dateDataValue}).then((data) => {
      setScheduleData(data)
      setError(null)
    }).catch((err) => {
      setError(err.message)
    }).finally(() => {
      setLoading(false)
    })
   
  }, [groupDataValue, dateDataValue])

  // загружаем расписание при монтировании расписания
  useEffect(() => {
    loadSchedule()
  }, [loadSchedule])


  // загружает информацию о наличии домашек 
  const loadAllHomeworkStatus = async (scheduleData) => {
    setHomeworkExistsMap({}) // обнуляем при загрузке изначально, чтобы не было ложных подсвечиваний
    if (!scheduleData) return
    const currentAPI = notesEnabled ? API.notes : API.homework

    const homeworksMap = await currentAPI.getPresence(
      groupDataValue,
      scheduleDateDataValue,
    ) 
    setHomeworkExistsMap(homeworksMap)
  }

  const currentHomeworkExists = (currentHomeworkIndex) => {
    return homeworkExistsMap[currentHomeworkIndex] ?? false
  }
  

  useEffect( () => {
    loadAllHomeworkStatus(scheduleData)
  }, [scheduleData, notesEnabled])


  // Обработчик клика по домашке
  const handleHomeworkClick = (lessInfo) => {
    const {
      groupDataValue,
      lessonIndex,
      lessonDate,
      lessonName,
    } = lessInfo

    const currentAPI = notesEnabled? API.notes : API.homework 
    
    currentAPI
      .get(groupDataValue, scheduleDateDataValue, lessonIndex)
      .then((resp) => {
        const { homework_text, updated, username } = resp
        console.log('FROM SCHEDULECONT resp :>> ', resp);
        console.log('FROM SCHEDULECONT currentAPI :>> ', currentAPI);
        setHomeworkUpdated(updated)
        setHomeworkText(homework_text)
        setHomeworkAuthor(username)
      }).catch( (error) => {
        setHomeworkText('')
        showNotificationOuter(error.message, 'error')
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
  const getDayClass = (dateText) => {
    if (!dateText) return ""

    const monthsMap = {
      января: 0,
      февраля: 1,
      марта: 2,
      апреля: 3,
      мая: 4,
      июня: 5,
      июля: 6,
      августа: 7,
      сентября: 8,
      октября: 9,
      ноября: 10,
      декабря: 11,
    }

    const normalizedDateText = dateText.trim()
    const [rawOnlyDay, rawMonth] = normalizedDateText.split(" ")
    const dayNumber = parseInt(rawOnlyDay.replace(/\D/g, ""), 10)
    const monthKey = rawMonth?.toLowerCase()
    const monthIndex = monthKey ? monthsMap[monthKey] : undefined

    if (Number.isNaN(dayNumber) || monthIndex === undefined) {
      return ""
    }

    const currentDate = new Date()
    const isCurrentDate =
      currentDate.getDate() === dayNumber &&
      currentDate.getMonth() === monthIndex

    return isCurrentDate ? "active-day" : ""
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

  
  // Рендер десктоп расписания
  const renderDesktopSchedule = (scheduleData) => {
    if (!scheduleData) return null

    const datesArr = scheduleData.days.map((day) => day.date)
    let currentLessonIndex = 0

    return (
      <table
        className={`table ${darkTheme ? " dark" : ""}`}
        id="schedule-container"
      >
        <thead>
          <tr className="table_row_high">
            <th>время</th>
            {scheduleData.days.map((day, index) => (
              <th key={index} className={getDayClass(day.date)}>
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
                currentLessonIndex++

                const lessonInfo = {
                  groupDataValue: groupDataValue,
                  dateDataValue: getDateValueFromDisplay(datesArr[dayIndex]),
                  lessonIndex: currentLessonIndex,

                  // lessonName передается как пропс для HomeworkModal и исп. только там
                  lessonName: dayLessons.map(
                    (lesson, index) => {
                      let currentLessonName = lesson.text.split(", ").slice(0, 2).join(", ") 

                      if (index < dayLessons.length - 1) currentLessonName += ', '
                      return currentLessonName
                    }
                  ),
                  lessonDate: dataDate,
                }

                return (
                  <td
                    key={`${timeIndex}-${dayIndex}`}
                    data-date={dataDate}
                    data-ind={currentLessonIndex}
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

                        return (
                          <div
                            key={lessonIndex}
                            className={`lesson-item${currentHomeworkExists(currentLessonIndex) ? ' active' : ''}`}
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
                              className={`homework${currentHomeworkExists(currentLessonIndex) ? ' active' : '' }`}
                              onClick={() => {
                                handleHomeworkClick(lessonInfo)
                              }}
                              style={{ cursor: "pointer" }}
                              title={"домашнее задание"}
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

  // рендер мобильного расписания
  const renderMobileSchedule = (scheduleData) => {
    if (!scheduleData) return null 

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

        onClick={() => handleHomeworkClick({
          groupDataValue: groupDataValue,
          dateDataValue: scheduleDateDataValue,
          lessonIndex: lessonId,
          lessonName: lesson?.map(sublesson => (sublesson.text)).slice(0, 2).join(", "),
          lessonDate: datesArr[weekDayIndex],
        })}

        hasHomework={currentHomeworkExists(lessonId)}
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
          homeworkExistsMap={homeworkExistsMap}
        />
      )}
    </>
  )
}

export default ScheduleContainer
