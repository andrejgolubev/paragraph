const BASE_URL = "http://127.0.0.1:8000"
const headers = { "Content-Type": "application/json"}

const homeworkAPI = {
  saveHomework: async (groupDataValue, dateDataValue, lessonIndex, homeworkText) => {
    
    const payload = {
      group_data_value: String(groupDataValue),
      date_data_value: String(dateDataValue),
      lesson_index: Number(lessonIndex),
      homework: String(homeworkText),
    };
    
    const response = await fetch(`${BASE_URL}/homework/save`, {
      method: "POST",
      headers: { 
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
      credentials: 'include',
    });
    
    
    const responseData = await response.json();
    console.log("responseData:", responseData)
    console.log("responseData.detail:", responseData.detail)

    return responseData;
      
    
  },


  loadHomeworkData: async function loadHomeworkData(
    groupDataValue,
    dateDataValue,
    lessonIndex
  ) {
    const params = new URLSearchParams({
      group_data_value: String(groupDataValue),
      date_data_value: dateDataValue,
      lesson_index: parseInt(lessonIndex),
    })

    return fetch(`${BASE_URL}/homework/get?${params.toString()}`, {
      method: "GET",
      credentials: "include"
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

  sendRegisterData: async (email, password, username, group) => {
    return fetch(`${BASE_URL}/user/register`, {
      method: "POST",
      headers,
      credentials: 'include',
      body: JSON.stringify({
        username,
        email,
        password,
        group_number: group,
      }), 
    })
  }, 
  sendLoginData: async (email, password) => {
    return fetch(`${BASE_URL}/user/login`, {
      method: "POST", 
      headers, 
      body: JSON.stringify({
        email,
        password,
      }), 
      credentials: 'include'
    })
  } 
}

export default homeworkAPI
