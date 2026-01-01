const BASE_URL = "http://127.0.0.1:8000"
const headers = { "Content-Type": "application/json"}

const homeworkAPI = {
  saveHomework: (groupDataValue, dateDataValue, lessonIndex, homeworkText) => {
    return fetch(`${BASE_URL}/homework/save`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        group_data_value: String(groupDataValue),
        date_data_value: dateDataValue,
        lesson_index: lessonIndex,
        homework: homeworkText,
      }),
    })
  },

  loadHomeworkData: async function loadHomeworkData(
    groupDataValue,
    dateDataValue,
    lessonIndex
  ) {
    const params = new URLSearchParams({
      group_data_value: String(groupDataValue),
      date_data_value: dateDataValue,
      lesson_index: lessonIndex,
    })

    // console.log('http://127.0.0.1:8000/homework/get?${params.toString() :>> ', `http://127.0.0.1:8000/homework/get?${params.toString()}`)
    return fetch(`${BASE_URL}/homework/get?${params.toString()}`, {
      method: "GET",
    })
      .then((resp) => resp.json())
      .catch((e) => console.error(e))
  },

  loadGroups: async function loadGroups() {
    return fetch(`${BASE_URL}/schedule/get-all-groups`)
      .then((response) => response.json())
      .catch((err) => {
        console.log("Error loading dates:", err)
        return []
      })
  },

  loadDates: async function loadDates() {
    return fetch(`${BASE_URL}/schedule/get-all-dates`)
      .then((response) => response.json())
      .catch((err) => {
        console.log("Error loading dates:", err)
        return []
      })
  },

  convertToDataValue: async ({ groupNumber = "", date = "" }) => {
    console.log("groupNumber selected in convertToDataValue :>> ", groupNumber)

    const params = new URLSearchParams({
      group_number: String(groupNumber),
      date: date,
    })
    const url = `${BASE_URL}/homework/convert?${params.toString()}`
    console.log("url :>> ", url)
    return fetch(url, {
      method: "GET",
    })
      .then((resp) => resp.json())
      .catch((e) => console.error(e))
  },

  convertFromDataValue: async ({ groupDataValue, dateDataValue }) => {
    const params = new URLSearchParams({
      group_data_value: String(groupDataValue),
      date_data_value: dateDataValue,
    })

    const resp = await fetch(
      `${BASE_URL}/homework/convert-back?${params.toString()}`,
      {
        method: "GET",
      }
    )
    const response = await resp.json()
    return response
  },

  getAllGroups: async () => {
    return fetch(`${BASE_URL}/schedule/get-all-groups`).then((resp) =>
      resp.json()
    ).catch(err => console.log(err))
  },
}

export default homeworkAPI
