import axios from 'axios'

async function checkToken() {
  return axios({
    url: 'http://localhost:8000/checkauth',
    method: 'GET',
    params: {
      token: localStorage.token
    }
  })
}
