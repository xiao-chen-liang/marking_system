import {createRouter, createWebHistory} from 'vue-router'
import ReportCard from "../views/ReportCard.vue";
import ScoreItem from "../views/ScoreItems.vue";
import Score from "../views/Score.vue"
import Ranking from '../views/Ranking.vue'
import login from '../views/Login.vue'
import register from '../views/Register.vue'
import modify from '../views/Modify.vue'
import dashboard from "@/views/Dashboard.vue";


const routes = [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
    {
        path: '/modify',
        name: 'modify',
        component: modify
    },
    {
        path: '/dashboard',
        name: 'dashboard',
        component: dashboard,
        redirect: '/dashboard/report-card',
        children: [
            {
                path: '/dashboard/report-card',
                name: 'report-card',
                // component: HomeView
                component: ReportCard
            },
            {
                path: '/dashboard/score-item',
                name: 'score-item',
                component: ScoreItem
            },
            {
                path: '/dashboard/score',
                name: 'score',
                component: Score
            },
            {
                path: '/dashboard/ranking',
                name: 'ranking',
                component: Ranking
            },
        ]
    },

    // {
    //   path: '/',
    //   name: 'home',
    //   // component: HomeView
    //   component: ReportCard
    // },
    //     {
    //   path: '/score-item',
    //   name: 'score-item',
    //   component: ScoreItem
    //   },
    // {
    //   path: '/score',
    //   name: 'score',
    //   component: Score
    // },
    // {
    //   path: '/ranking',
    //   name: 'ranking',
    //   component: Ranking
    // },
    //   // catch all 404
    // {
    //   path: '/:catchAll(.*)',
    //   name: 'not-found',
    //   component: NotFoundView
    // },
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
