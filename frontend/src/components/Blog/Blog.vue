<template>
  <div>
    <Header></Header>
    <el-row class="main_container">
    <el-row>
      <el-col :span="4" :offset="2">
        <el-button type="primary" icon="el-icon-back" @click="return_button_clicked">返回博客页面</el-button>
      </el-col>
    </el-row>
    <el-row>
      <center>
      <el-col class="title">
        <span> {{ blog.title }} </span>
      </el-col>
    </center>
    </el-row>
    <el-row class="label_container">
      <el-col :span="2" :offset="14">
        <span class="label">· {{ blog.category }} </span>
      </el-col>
      <el-col :span="6">
        <span class="label">· 发布于 {{ blog.post_time }} </span>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="20" :offset="2">
        <hr width="100%" style="height:1px;border:none;border-top: 1px solid #E4E7ED;float:left;margin-top: 0px"/>
      </el-col>
    </el-row>
    <el-row class="editor_container">
      <el-col :offset="2" :span="20">
      <mavon-editor :ishljs="true" v-model="blog.content" class="editor" :subfield="false" default_open="preview" :toolbars="toolbars"></mavon-editor>
      </el-col>
    </el-row>
    </el-row>
  </div>
</template>

<script type="text/javascript">
/* eslint-disable camelcase */
import Header from '../general/Header.vue'
import get_url from '../general/getUrl.js'
import $ from 'jquery'
export default {
  name: 'Blog',
  components: { Header },
  data () {
    return {
      blog: {
        title: '',
        post_time: '',
        category: '',
        content: ''
      },
      toolbars: {
        readmodel: true
      }
    }
  },
  methods: {
    return_button_clicked: function () {
      this.$router.push({ path: '/blog' })
    }
  },
  beforeCreate: function () {
    var post_url = get_url(this.$store.state.dev, '/journal/info_all/')
    var post_data = { id: this.$route.params.blog_id }
    var _this = this
    $.ajax({
      ContentType: 'application/json; charset=utf-8',
      dataType: 'json',
      url: post_url,
      data: post_data,
      type: 'POST',
      success: function (data) {
        var info = data['info']
        _this.blog.title = info.title
        _this.blog.post_time = info.post_time
        _this.blog.content = info.content
        _this.blog.category = info.category
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
  .editor{
    height: 600px;
  }
  .main_container{
    margin-top: 25px;
  }
  .title{
    font-size: 28px;
    color: #303133;
  }
  .label_container{
    color: #606266;
    margin: 20px 0px 10px 0px;
  }
  .label{
    font-size: 18px;
  }
  .editor_container{
    margin-top: 20px;
  }
</style>