import axios from 'axios';

const instance = axios.create();

// Add a request interceptor
instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('userToken');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }

    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// Add a response interceptor
instance.interceptors.response.use(
  response => {
    // Check if the response is successful (status code within 2xx range)
    if (response.status >= 200 && response.status < 300) {
      // Assuming the token is returned in response.data.token
      const { token } = response.data;
      if (token) {
        // Store the token in localStorage
        localStorage.setItem('userToken', token);
      }
    }
    return response;
  },
  error => {
    // Handle errors here
    if (error.response && error.response.status === 401) {
      // Handle token expiration, e.g., redirect to login page
      localStorage.removeItem('userToken');
      alert(error.response.data.message);
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default instance;
