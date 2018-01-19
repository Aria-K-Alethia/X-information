<template>
  <div>
    <el-row type="flex" class="head">
      <el-col :span="2" :offset="11">
        <center>
          <span style="font-size: 24px;color: #303133;">消 息 版</span>
        </center>
      </el-col>
      <el-col :span="4" :offset="2">
        <el-button type="primary" icon="el-icon-refresh" @click="noti_refresh_button_clicked">点击刷新信息</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <center>
          <hr width="90%" style="height: 1px;border: none; border-top: 1px solid #DCDFE6;margin-bottom: 40px;"/>
        </center>
      </el-col>
    </el-row>
    <el-row type="flex" justify="center">
      <el-col :span="24">
    <div class="noti_container">
      <template v-for="(noti,index) in notifications">
        <el-row type="flex">
          <el-col :span="10" :offset="7">
        
        <el-card class="noti_card">
          <div slot="header">
            <i class="el-icon-info"></i>
            <span class="noti_head"> 来自<span style="color:#606266"> {{ noti.from }} </span> 的信息</span>
            <el-button type="text" @click="noti_del_button_clicked(noti.id,index)" style="padding: 5px 0px 0px 0px;float:right;font-size: 16px;" icon="el-icon-delete">
            </el-button>
          </div>
          <el-row>
          <el-button type="text" @click="noti_button_clicked(noti.link)" class="noti_button">
          <div class="overview">
            <p>{{ noti.overview }}</p>
          </div>
          </el-button>
        </el-row>
        <el-row>
          <div class="time"> 
            发布于 {{ noti.time }} 
          </div>
        </el-row>
        </el-card>
      
      <hr width="100%" style="height:1px;border:none;border-top: 1px solid #E4E7ED"/>
    </el-col>
  </el-row>
      </template>
    </div>
  </el-col>
</el-row>
  </div>
</template>

<script type="text/javascript">
/* eslint-disable camelcase */
import $ from 'jquery'
import get_url from '../general/getUrl.js'
export default {
  name: 'Notification',
  data () {
    return {
      notifications: []
    }
  },
  methods: {
    check_login: function () {
      if (this.$store.state.is_login) return true
      else {
        this.$message({
          showClose: true,
          type: 'error',
          message: '请先登录'
        })
        return false
      }
    },
    noti_button_clicked: function (link) {
      window.open(link)
    },
    noti_del_button_clicked: function (id, index) {
      if (!this.check_login() && !this.$store.state.dev) return
      this.$confirm('删除这条信息吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        var post_url = get_url(this.$store.state.dev, '/notification/delete/')
        var post_data = { 'id': id }
        var _this = this
        $.ajax({
          ContentType: 'application/json; charset=utf-8',
          dataType: 'json',
          url: post_url,
          type: 'POST',
          data: post_data,
          success: function (data) {
            var code = data['code']
            if (code === 0) {
              _this.$message({
                showClose: true,
                type: 'success',
                message: '删除成功'
              })
              _this.notifications.splice(index, 1)
            } else if (code === 1) {
              _this.$message({
                showClose: true,
                type: 'error',
                message: '删除失败'
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
      })
    },
    noti_refresh_button_clicked: function () {
      var post_url = get_url(this.$store.state.dev, '/notification/refresh/')
      var _this = this
      $.ajax({
        ContentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: post_url,
        type: 'POST',
        success: function (data) {
          var code = data['code']
          if (code === 0) {
            var begin_id = data['begin_id']
            post_url = get_url(_this.$store.state.dev, '/notification/newest/')
            var post_data = { begin_id: begin_id }
            $.ajax({
              ContentType: 'application/json; charset=utf-8',
              dataType: 'json',
              url: post_url,
              data: post_data,
              type: 'POST',
              success: function (data) {
                _this.notifications = []
                var info_list = data['info_list']
                for (var i = 0; i < info_list.length; i++) {
                  var temp = {}
                  temp.id = info_list[i].id
                  temp.from = info_list[i].noti_from
                  temp.overview = info_list[i].overview
                  temp.time = info_list[i].post_time
                  temp.link = info_list[i].link
                  _this.notifications.push(temp)
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
          } else if (code === 1) {
            _this.$message({
              showClose: true,
              type: 'info',
              message: '暂时没有新消息噢'
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
    var post_url = get_url(this.$store.state.dev, '/notification/history/')
    var temp = new Date()
    var from_time = [temp.getFullYear(), temp.getMonth() + 1, temp.getDate(), temp.getHours()].join(' ')
    var post_data = { 'from_time': from_time }
    var _this = this
    $.ajax({
      ContentType: 'application/json; charset=utf-8',
      dataType: 'json',
      url: post_url,
      type: 'POST',
      data: post_data,
      success: function (data) {
        var info_list = data['info_list']
        for (var i = 0; i < info_list.length; i++) {
          var temp = {}
          temp.id = info_list[i].id
          temp.from = info_list[i].noti_from
          temp.overview = info_list[i].overview
          temp.time = info_list[i].post_time
          temp.link = info_list[i].link
          _this.notifications.push(temp)
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
}
</script>

<style type="text/css" scpoed>
  .noti_container{
    width: auto;
  }
  .noti_button{
    padding: 0px 0px 0px 0px;
    text-align: left;
    color: #303133;
    font-size: 18px;
  }
  .noti_button:hover{
    color: #409EFF;
  }
  .head{
    margin: 20px 0px 10px 0px;
  }
  .overview{
    padding: 0px 0px 10px 0px;
    word-wrap: break-word;
    word-break: break-all;
    white-space: pre-line;
    text-align: left;
    line-height: 20px;
  }
  .noti_head{
    color: #303133;
    padding: 0px 0px 0px 0px;
  }
  .time{
    font-size: 14px;
    float: right;
    padding-bottom: 10px;
    padding-top: 10px;
    color: #909399;
  }
</style>