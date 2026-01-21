import { BASE_URL, headers, getHandledResponseData, fetchUrl } from "./API"


async function authApiFetch(url, options = {}, additional = {}) {
  const response = await fetchUrl(url, options)

  const responseData = await getHandledResponseData(response)

  return { ...responseData, ...additional }
}


const authAPI = {
  sendRegisterData: async (
    email,
    password,
    username,
    group,
    acceptPd,
    acceptTerms
  ) => {
    return authApiFetch(
      `${BASE_URL}/user/register`,
      {
        method: "POST",
        headers,
        body: JSON.stringify({
          username,
          email,
          password,
          group_number: group,
          accept_pd: acceptPd,
          accept_terms: acceptTerms,
        }),
      },
      {
        type: "sign-up",
      }
    )
  },

  sendLoginData: async (email, password) => {
    const url = `${BASE_URL}/user/login`
    return authApiFetch(
      url,
      {
        method: "POST",
        headers,
        body: JSON.stringify({
          email,
          password,
        }),
      },
      { type: "sign-in" }
    )
  },
}

export default authAPI