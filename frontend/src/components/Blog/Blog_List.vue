<template>
  <div>
    <Header></Header>
    <el-row class="main_container">
    <el-row>
      <el-col :span="4" :offset="10">
        <span class="head">日志列表</span>
      </el-col>
      <el-col :span="4">
        <el-button type="primary" icon="el-icon-plus" @click="write_blog_button_clicked">写新日志</el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <center>
          <hr width="90%" style="height: 1px;border: none; border-top: 1px solid #DCDFE6;margin-bottom: 40px; margin-top: 20px"/>
        </center>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="20" :offset="2">
        <el-table :data="blog_table_data" style="width:100%" height="250">
          <el-table-column prop="category" label="类型" sortable align="center"></el-table-column>
          <el-table-column prop="title" label="标题" align="center"></el-table-column>
          <el-table-column prop="date" label="发布日期" sortable align="center"></el-table-column>
          <el-table-column fixed="right" label="操作" align="center">
            <template slot-scope="scope">
              <el-button @click="view_blog_button_clicked(scope.$index)" type="text" icon="el-icon-view" class="button"></el-button>
              <el-button @click="edit_blog_button_clicked(scope.$index)" type="text" icon="el-icon-edit-outline" class="button"></el-button>
              <el-button @click="delete_blog_button_clicked(scope.$index)" type="text" icon="el-icon-delete" class="button"></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-col>
    </el-row>
  </el-row>
    <!-- insert/edit dialog -->
    <el-dialog :visible="editor.dialog_visible" fullscreen center show-close :before-close="handle_close">
    <span slot="title" class="dialog_head">
      {{ editor.dialog_title }}
    </span>
    <el-row>
      <el-col :span="4" :offset="2">
      <p class="label">
        选择博客的类型:
      </p>
      </el-col>
      <el-col :span="18">
        <el-radio-group v-model="editor.category" style="padding-top: 22px">
          <el-radio :label="0">学习报告</el-radio>
          <el-radio :label="1">读书笔记</el-radio>
        </el-radio-group>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="20" :offset="2">
        <hr width="100%" style="height:1px;border:none;border-top: 1px solid #E4E7ED;float:left"/>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4" :offset="2">
      <p class="label">
        标题
      </p>
    </el-col>
    </el-row>
    <el-row tpye='flex' justify="center">
      <el-col :span="20" class="input" :offset="2">
        <el-input v-model="editor.title" placeholder="输入标题,4-30个字符">
        </el-input>
      </el-col>
    </el-row>
        <el-row>
      <el-col :span="20" :offset="2">
        <hr width="100%" style="height:1px;border:none;border-top: 1px solid #E4E7ED;float:left;margin-top: 20px"/>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="4" :offset="2">
      <p class="label">
        正文
      </p>
    </el-col>
    </el-row>
    <el-row>
      <el-col :offset="2" :span="20">
      <mavon-editor :ishljs="true" v-model="editor.content" class="editor"></mavon-editor>
    </el-col>
    </el-row>
      <span slot="footer">
        <el-button @click="editor.dialog_visible = false">取消</el-button>
        <el-button type="primary" @click="commit_blog_button_clicked">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script type="text/javascript">
/* eslint-disable camelcase */
import Header from '../general/Header.vue'
import get_url from '../general/getUrl.js'
import $ from 'jquery'
export default {
  name: 'Blog_List',
  components: { Header },
  data () {
    return {
      blog_table_data: [],
      editor: {
        dialog_visible: false,
        dialog_title: '',
        content: '',
        category: '',
        title: '',
        id: -1
      },
      is_insert: true
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
    write_blog_button_clicked: function () {
      if (!this.check_login() && !this.$store.state.dev) return
      this.is_insert = true
      this.editor.dialog_title = '写新日志'
      this.editor.content = ''
      this.editor.category = ''
      this.editor.title = ''
      this.editor.id = -1
      this.editor.dialog_visible = true
    },
    edit_blog_button_clicked: function (index) {
      if (!this.check_login() && !this.$store.state.dev) return
      this.is_insert = false
      this.editor.dialog_title = '修改日志'
      this.editor.id = this.blog_table_data[index].id
      this.editor.category = this.blog_table_data[index].category === '学习报告' ? 0 : 1
      this.editor.title = this.blog_table_data[index].title
      var post_url = get_url(this.$store.state.dev, '/journal/info/')
      var post_data = { id: this.editor.id }
      var _this = this
      $.ajax({
        ContentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: post_url,
        type: 'POST',
        data: post_data,
        success: function (data) {
          console.log(data)
          _this.editor.content = data['content']
          _this.editor.dialog_visible = true
        },
        error: function () {
          _this.$message({
            showClose: true,
            type: 'error',
            message: '无法连接服务器'
          })
        }
      })
    },
    view_blog_button_clicked: function (index) {
      this.$router.push({ path: '/blog/' + this.blog_table_data[index].id })
    },
    delete_blog_button_clicked: function (index) {
      if (!this.check_login() && !this.$store.state.dev) return
      this.$confirm('删除这条信息吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        var post_url = get_url(this.$store.state.dev, '/journal/delete/')
        var post_data = { 'id': this.blog_table_data[index].id }
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
              _this.blog_table_data.splice(index, 1)
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
              message: '无法连接服务器'
            })
          }
        })
      })
    },
    commit_blog_button_clicked: function () {
      var post_url
      var post_data
      var _this = this
      if (!this.is_insert) {
        post_url = get_url(this.$store.state.dev, '/journal/modify/')
      } else {
        post_url = get_url(this.$store.state.dev, '/journal/insert/')
      }
      post_data = { id: this.editor.id, title: this.editor.title, category: this.editor.category, content: this.editor.content }
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
              message: '操作成功'
            })
            this.editor.content = ''
            this.editor.category = ''
            this.editor.title = ''
            this.editor.id = -1
            this.editor.dialog_visible = false
          } else if (code === 1) {
            _this.$message({
              showClose: true,
              type: 'error',
              message: '操作失败了呢'
            })
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
    },
    handle_close: function (done) {
      this.editor.dialog_visible = false
      done()
    }
  },
  beforeCreate: function () {
    var post_url = get_url(this.$store.state.dev, '/journal/id_list/')
    var _this = this
    $.ajax({
      ContentType: 'application/json; charset=utf-8',
      dataType: 'json',
      url: post_url,
      type: 'POST',
      success: function (data) {
        var id_list = data['id_list']
        for (var i = 0; i < id_list.length; i++) {
          var temp = {}
          temp.id = id_list[i].id
          temp.category = id_list[i].category
          temp.title = id_list[i].title
          temp.date = id_list[i].post_time
          _this.blog_table_data.push(temp)
        }
      },
      error: function () {

      }
    })
  }
}
</script>

<style type="text/css" scoped>
  .main_container{
    margin-top: 20px;
  }
  .head{
    font-size: 24px;
    color: #303133;
  }
  .button{
    font-size: 18px;
    padding: 0px 5px 0px 0px;
  }
  .editor{
    height: 600px;
  }
  .label{
    font-size: 18px;
  }
  .dialog_head{
    font-size: 24px;
    color: #303133;
  }
</style>