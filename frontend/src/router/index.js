/* eslint-disable camelcase */
import Vue from 'vue'
import ElementUI from 'element-ui'
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
import 'element-ui/lib/theme-chalk/index.css'
import Router from 'vue-router'
import Index from '@/components/Index.vue'
import Book from '@/components/Book/Book.vue'
import Blog_List from '@/components/Blog/Blog_List.vue'
import Blog from '@/components/Blog/Blog.vue'
import Graph from '@/components/Graph/Graph.vue'

Vue.use(ElementUI)
Vue.use(Router)
Vue.use(mavonEditor)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index
    },
    {
      path: '/index',
      name: 'index',
      component: Index
    },
    {
      path: '/book',
      name: 'book',
      component: Book
    },
    {
      path: '/blog',
      name: 'blog_list',
      component: Blog_List
    },
    {
      path: '/blog/:blog_id',
      name: 'blog',
      component: Blog
    },
    {
      path: '/graph/',
      name: 'graph',
      component: Graph
    }
  ]
})
