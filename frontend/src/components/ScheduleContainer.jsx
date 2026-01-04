import { useState, useEffect, useCallback } from "react"
import HomeworkModal from "./HomeworkModal" // Предполагаем, что модалка уже переписана на React
import paperclip from "../images/homework/paperclip.svg"
import { useContext } from "react"
import { Context } from "../context/Provider"
import homeworkAPI from "../api/homeworkAPI"
import { Mosaic } from "react-loading-indicators"
import { getDateValueFromDisplay, getLessonTypeClass } from "../utils/converters"

let lessonInfoGlobal = {}

const ScheduleContainer = () => {
  const { groupDataValue, dateDataValue, setGroupDataValueCookies } = useContext(Context)
  const [scheduleData, setScheduleData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedLesson, setSelectedLesson] = useState(null)
  const [showDialog, setShowDialog] = useState(false)
  const [homeworkText, setHomeworkText] = useState("")
  const [homeworkUpdated, setHomeworkUpdated] = useState("")
  const [year, setYear] = useState(new Date().getFullYear())

  useEffect(() => {
    setGroupDataValueCookies('groupDataValue', groupDataValue, {maxAge: 60*60*24*14}) // чтобы сразу загружалась нужная группа 
    
    // логирование - потом убрать
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
    try {
      setLoading(true)
      
      let url = `http://127.0.0.1:8000/schedule/get-schedule?group_data_value=${groupDataValue}`
      if (dateDataValue) {
        url += `&date_data_value=${dateDataValue}`
      }
      
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`HTTP error. ${response}`)
      }
      
      const data = await response.json()
      
      console.log('data (from schedulecont) :>> ', data);
      
      setScheduleData(data)
      
      setError(null)
    } catch (err) {
      console.error("Error loading schedule:", err)
      setError(err.message)
      console.log('error :>> ', error);
    } finally {
      setLoading(false)
    }
  }, [groupDataValue, dateDataValue])

  // загружаем расписание при монтировании расписания
  useEffect(() => {
    loadSchedule()
  }, [loadSchedule])

  // Обработчик клика по домашке
  const handleHomeworkClick = (lessInfo) => {
    const {
      groupDataValue,
      dateDataValue,
      lessonIndex,
      lessonDay,
      lessonName,
    } = lessInfo

    homeworkAPI
      .loadHomeworkData(groupDataValue, scheduleDateDataValue, lessonIndex)
      .then((resp) => {
        const { homework, updated } = resp
        setHomeworkUpdated(updated)
        setHomeworkText(homework)
      }).catch( () => {
        setHomeworkUpdated('')
      }
      )

    const lessonInfo = {
      groupDataValue,
      dateDataValue,
      lessonIndex: parseInt(lessonIndex),
      lessonDay,
      lessonName,
    }

    setSelectedLesson(lessonInfo)

    lessonInfoGlobal = { ...lessonInfo, dateDataValue: scheduleDateDataValue }
    
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

  // Рендер расписания
  const renderSchedule = () => {
    if (!scheduleData) return null

    const datesArr = scheduleData.days.map((day) => day.date)
    let lessonIndex = 1

    return (
      <table className="table" id="schedule-container">
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
                const currentLessonIndex = lessonIndex++

                return (
                  <td
                    key={`${timeIndex}-${dayIndex}`}
                    data-date={dataDate}
                    data-index={currentLessonIndex}
                  >
                    {dayLessons.length > 0 ? (
                      dayLessons.map((lesson, lessonIndex) => {
                        const lessonId =
                          lesson.type === "Лек."
                            ? "lec"
                            : lesson.type === "Упр."
                            ? "upr"
                            : lesson.type === "Лаб."
                            ? "lab"
                            : "default"

                        const lessonInfo = {
                          groupDataValue: groupDataValue,
                          dateDataValue: getDateValueFromDisplay(
                            datesArr[dayIndex]
                          ),
                          lessonIndex: currentLessonIndex,
                          lessonName: lesson.text.split(", ")[0],
                          lessonDay: dataDate,
                        }

                        return (
                          <div
                            key={lessonIndex}
                            className="lesson-item"
                            id={lessonId}
                          >
                            {lesson.type && (
                              <span
                                className={`lesson-type ${getLessonTypeClass(
                                  lesson.type
                                )}`}
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
                              <img src={paperclip} alt="Homework" />
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

  // Состояния загрузки и ошибки
  if (loading) {
    return (
      <>
        <div className="schedule-container loading"></div>
        <div className="loading-indicator">
          <Mosaic
            color="#FFF"
            size="large"
            text="загрузка..."
            textColor="#CBCBDE"
          />
        </div>
      </>
    )
  }

  if (error) {
    return ( 
      <div className="schedule-container error">
        <div className="tip active">
          <button 
          style={{background: '#FFFFFF', padding: '4px', border: '2px rgb(207, 222, 227) dashed', position: 'absolute', 'border-radius': '8px'}} 
          onClick={loadSchedule}>
            <p>{error}</p>
            <p>произошла ошибка. нажмите сюда, </p>
            <p>чтобы попробовать снова</p>
          </button>
        </div>
      </div>
    )
  }

  return (
    <>
      <div
        className={`schedule-container ${scheduleData ? "loaded" : "loading"}`}
      >
        {renderSchedule()}
      </div>

      {/* Модальное окно домашнего задания */}
      {showDialog && (
        <HomeworkModal
          lessonInfo={lessonInfoGlobal}
          homeworkText={homeworkText}
          homeworkUpdated={homeworkUpdated}
          setHomeworkUpdated={setHomeworkUpdated}
          showDialog={showDialog}
          setShowDialog={setShowDialog}

        />
      )}
    </>
  )
}

export default ScheduleContainer
