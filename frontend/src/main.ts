import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import './styles/style.scss';

import Vue3Toastify, { type ToastContainerOptions } from 'vue3-toastify';
import 'vue3-toastify/dist/index.css';


const app = createApp(App);

const toastOptions: ToastContainerOptions = {
  autoClose: 3000,
  position: 'top-right',
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
};

app.use(Vue3Toastify, toastOptions);
app.use(router);
app.mount('#app');
