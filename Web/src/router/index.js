import Vue from 'vue'
import Router from 'vue-router'
import login from "../views/auth/login";
import mail from "../views/mail/mail";


Vue.use(Router)

let router = new Router({
  routes: [
    {
      path: '/',
      name: 'auth',
      component: login
    },
    {
      path: '/mail',
      name: 'mail',
      component: mail
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (to.path !== '/') {
    //是否需要登录权限
    if (localStorage.token) {
      next()
    } else {
      next({
        path: '/',
      })
    }
  } else
    next()
})

export default router;
