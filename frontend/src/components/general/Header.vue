<template>
  <div>
    <el-row class="header_container">
      <el-col :span="4">
        <el-button type="text" @click.native="logo_button_clicked" class="logo">
          {{ logo_name }}
        </el-button>
      </el-col>
      <el-col :span="1">
        <hr style="height:40px;width:1px;border: none;border-left: 1px solid #ccc"/>
      </el-col>
      <el-col :span="15">
        <el-menu class="menu" mode="horizontal" @select="menu_selected">
          <el-menu-item index="index" class="menu_item" style="margin-right: 20px;">首页</el-menu-item>
          <el-menu-item index="book" class="menu_item" style="margin-right: 20px;">书籍</el-menu-item>
          <el-menu-item index="blog" class="menu_item" style="margin-right: 20px;">日志</el-menu-item>
          <el-menu-item index="graph" class="menu_item">统计图表</el-menu-item>
        </el-menu>
      </el-col>
      <el-col :span="2" :offset="2">
        <el-dropdown trigger="click">
          <span class="el-dropdown-link">
            <el-button type="text" v-if="!is_login" class="dropdown_button">登录 | 注册</el-button>
            <el-button type="text" v-else class="dropdown_button">{{ username }}</el-button>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item @click.native="login_button_clicked" v-if="!is_login">
            登录
          </el-dropdown-item>
            <el-dropdown-item @click.native="logout_button_clicked" v-else>
              登出
            </el-dropdown-item>
            <el-dropdown-item divided @click.native="register_button_clicked" v-if="!is_login">
              注册
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-col>
    </el-row>
    <!-- login -->
    <el-dialog title="登录" :visible.sync="login_form_visible" :before-close="handle_login_form_close" >
    <el-form :model="login_form" label-position="left">
      <el-form-item type="text" label="用户名" :label-width="form_label_width">
        <el-input v-model="login_form.username" auto_complete="off" @keydown.enter.native.prevent="login_confirm_button_clicked"></el-input>
      </el-form-item>
      <el-form-item label="密码" :label-width="form_label_width">
        <el-input type="password" v-model="login_form.password" auto_complete="off" size="small" @keydown.enter.native.prevent="login_confirm_button_clicked"></el-input>
      </el-form-item>
    </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click.native="login_confirm_button_clicked('login_form')">确 定</el-button>
        <el-button @click.native="login_form_visible=false">取 消</el-button>
        
      </span>
  </el-dialog>
  </div>
</template>

<script type="text/javascript">
/* eslint-disable camelcase */
// import show_message from './Message.js'
import $ from 'jquery'
import get_url from './getUrl.js'
// import logo from '../../assets/logo.png'
export default {
  name: 'Header',
  data () {
    return {
      logo_name: 'X-information',
      is_login: false,
      login_form_visible: false,
      form_label_width: '100px',
      login_form: {
        username: '',
        password: ''
      },
      username: ''
    }
  },
  methods: {
    logo_button_clicked: function () {
      this.$router.push({ path: '/index' })
    },
    menu_selected: function (key, keyPath) {
      if (key === 'index') {
        this.$router.push({ path: '/index' })
      } else if (key === 'book') {
        this.$router.push({ path: '/book' })
      } else if (key === 'blog') {
        this.$router.push({ path: '/blog' })
      } else if (key === 'graph') {
        this.$router.push({ path: '/graph' })
      }
    },
    login_button_clicked: function () {
      this.login_form_visible = true
    },
    logout_button_clicked: function () {
      var _this = this
      var post_url = get_url(this.$store.state.dev, '/user/logout/')
      $.ajax({
        ContentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: post_url,
        type: 'POST',
        success: function (data) {
          var code = data['code']
          if (code === 0) {
            _this.$message({
              showClose: true,
              type: 'success',
              message: '登出成功'
            })
            _this.$store.state.is_login = false
            _this.$store.state.username = ''
            _this.username = ''
            _this.is_login = false
          } else if (code === 1) {
            _this.$message({
              showClose: true,
              type: 'error',
              message: '登出失败'
            })
          }
        },
        error: function () {
          _this.$message({
            showClose: true,
            type: 'error',
            message: '无法连接到服务器'
          })
        }
      })
    },
    register_button_clicked: function () {
      this.$message({
        showClose: true,
        type: 'error',
        message: '暂未开放注册'
      })
    },
    handle_login_form_close: function (done) {
      done()
    },
    login_confirm_button_clicked: function () {
      var post_url = get_url(this.$store.state.dev, '/user/login/')
      var post_data = this.login_form
      var _this = this
      $.ajax({
        ContentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: post_url,
        type: 'POST',
        data: post_data,
        success: function (data) {
          console.log(data)
          var code = data['code']
          if (code === 0) {
            _this.$message({
              showClose: true,
              type: 'success',
              message: '登录成功'
            })
            _this.login_form_visible = false
            _this.$store.state.is_login = true
            _this.is_login = true
            _this.$store.state.username = data['username']
            _this.username = data['username']
          } else if (code === 1) {
            _this.$message({
              showClose: true,
              type: 'error',
              message: '用户名或密码错误'
            })
          }
        },
        error: function () {
          _this.$message({
            showClose: true,
            type: 'error',
            message: '无法连接到服务器'
          })
        }
      })
    }
  },
  beforeCreate: function () {
    var _this = this
    var post_url = get_url(this.$store.state.dev, '/user/logged_in/')
    $.ajax({
      ContentType: 'application/json; charset=utf-8',
      dataType: 'json',
      url: post_url,
      type: 'POST',
      success: function (data) {
        console.log(data)
        _this.username = data['username']
        if (_this.username == null) {
          _this.is_login = false
          _this.$store.state.is_login = false
          _this.$store.state.user_name = ''
        } else {
          _this.is_login = true
          _this.$store.state.is_login = true
          _this.$store.state.user_name = _this.username
        }
      },
      error: function () {
        _this.$message({
          showClose: true,
          type: 'error',
          message: '无法连接服务器'
        })
      }
    })
  }
}
</script>

<style type="text/css" scpoed>
  .header_container{
    font-family: Microsoft Yahei Light,Microsoft Yahei;
    height: 60px;
  }
  .logo{
    height: 60px;
    font-size: 24px;
    font-weight: 500;
    color: #409EFF;
    padding-left:20px;
    border-right-width: 0px;
    width:auto;
  }
  .menu{
    border: none;
  }
  .menu_item {
    font-size: 22px;
    color:#5A5E66;
  }
  .dropdown_button {
    font-size: 14px;
    margin-top: 10px;
  }
</style>