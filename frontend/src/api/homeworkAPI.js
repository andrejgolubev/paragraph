const BASE_URL = "http://127.0.0.1:8000"

const homeworkAPI = {
  saveHomework: (groupDataValue, dateDataValue, lessonIndex, homeworkText) => {
    return fetch(`${BASE_URL}/homework/save`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        group_data_value: groupDataValue,
        date_data_value: dateDataValue,
        lesson_index: lessonIndex,
        homework: homeworkText,
      }),
    })
  },

  loadGroups: async function loadGroups() {
    return fetch("http://127.0.0.1:8000/schedule/get-all-groups")
      .then((response) => response.json())
      .catch((err) => {
        console.log("Error loading dates:", err)
        return []
      })
  },

  loadDates: async function loadDates() {
    return fetch("http://127.0.0.1:8000/schedule/get-all-dates")
      .then((response) => response.json())
      .catch((err) => {
        console.log("Error loading dates:", err)
        return []
      })
  },

  loadHomeworkData: async function loadHomeworkData({
    groupDataValue,
    dateDataValue,
    lessonIndex,
  }) {
    return fetch(`http://127.0.0.1:8000/homework/get`, {
      method: "GET",
      body: { groupDataValue, dateDataValue, lessonIndex },
    })
      .then((resp) => resp.json())
      .catch((e) => console.log(e))
  },
}

export default homeworkAPI
