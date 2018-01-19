<template>
  <div class="container">
    <Header></Header>
    <el-row class="head">
      <el-col :span="19" :offset="1">
        <span style="font-size: 24px;color: #303133;">书籍</span>
      </el-col>
      <el-col :span="2">
        <el-button type="primary" icon="el-icon-plus" @click="insert_book_button_clicked" size="medium">
        增加书目
        </el-button>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
        <center>
          <hr width="90%" style="height: 1px;border: none; border-top: 1px solid #DCDFE6;margin-bottom: 40px;"/>
        </center>
      </el-col>
    </el-row>
    <el-row>
      <el-col>
    <template v-for="(book,index) in books" >
      <el-row style="margin-bottom: 20px;">
        <el-col :span="22" :offset="1">
      <el-card>
      <el-row>
        <el-col :span="6">
          <img :src="book.img" class="image">
        </el-col>
        <el-row>
          <el-col :span="18">
            <el-row>
              <el-col :span="21">
                <span class="title">
                  {{ book.title }}
                </span>
              </el-col>
              <el-col :span="3">
                <el-button class="button" type="text" icon="el-icon-edit-outline" @click="edit_book_button_clicked(index,book.id)"></el-button>
                <el-button class="button" type="text" icon="el-icon-delete" @click="del_book_button_clicked(index,book.id)"></el-button>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <hr width="35%" style="height:1px;border:none;border-top: 1px solid #E4E7ED;float:left"/>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <span class="author">
                  {{ book.author }}
                </span>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <hr width="35%" style="height:1px;border:none;border-top: 1px solid #E4E7ED;float:left"/>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24" class="rate">
                <el-rate v-model="book.rate" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" :disabled="book.rate_disabled" :max="10" :low-threshold="4" :high-threshold="7" allow-half @change="handle_rate_change(book.id)" show-score>
                </el-rate>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <hr width="35%" style="height:1px;border:none;border-top: 1px solid #E4E7ED;float:left"/>
              </el-col>
            </el-row>
            <el-row class="comment_container">
              <el-col :span="24">
                <span class="comment">
                  {{ book.comment }}
                </span>
              </el-col>
            </el-row>
            <el-row>
              <el-col :span="24">
                <span class="time">
                  {{ book.time }}
                </span>
              </el-col>
            </el-row>
          </el-col>
        </el-row>
      </el-row>
      </el-card>
    </el-col>
  </el-row>
  <!--
      <center>
        <hr width="80%" style="height:1px;border:none;border-top: 1px solid #E4E7ED;margin:20px 0px 10px 0px;"/>
        </center>
    -->
    </template>
    </el-col>
  </el-row>
  <!-- insert dialog -->
  <el-dialog :title="dialog_title" :visible.sync="insert_book_form_visible">
  <el-form :model="insert_book_form" label-width="50px">
    <el-form-item label="标题">
      <el-input v-model="insert_book_form.title"></el-input>
    </el-form-item>
    <el-form-item label="作者">
      <el-input v-model="insert_book_form.author"></el-input>
    </el-form-item>
    <el-form-item label="评分">
      <el-rate v-model="insert_book_form.rate" :colors="['#99A9BF', '#F7BA2A', '#FF9900']" :max="10" :low-threshold="4" :high-threshold="7" allow-half show-score style="margin-top: 10px;">
      </el-rate>
    </el-form-item>
    <el-form-item label="评价">
      <el-input type="textarea" v-model="insert_book_form.comment">
      </el-input>
    </el-form-item>
    <el-form-item label="图片">
      <input type="file" value="" id="file" accept="image/*">
    </el-upload>
    </el-form-item>
  </el-form>
  <div slot="footer">
    <el-button type="primary" @click="insert_book_confirm_button_clicked">确 定</el-button>
    <el-button @click="insert_book_form_visible=false">取 消</el-button>
  </div>
  </el-dialog>

  </div>
</template>

<script type="text/javascript">
/* eslint-disable camelcase */
import Header from '../general/Header.vue'
import $ from 'jquery'
import get_url from '../general/getUrl.js'
export default {
  name: 'Book',
  components: { Header },
  data () {
    return {
      books: [],
      insert_book_form_visible: false,
      insert_book_form: {
        id: '',
        title: '',
        author: '',
        rate: 0,
        comment: ''
      },
      dialog_title: '',
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
    insert_book_button_clicked: function () {
      if (!this.check_login() && !this.$store.state.dev) return
      this.is_insert = true
      this.dialog_title = '增加新的条目'
      this.insert_book_form.title = ''
      this.insert_book_form.author = ''
      this.insert_book_form.rate = 0
      this.insert_book_form.comment = ''
      this.insert_book_form_visible = true
    },
    del_book_button_clicked: function (index, id) {
      if (!this.check_login() && !this.$store.state.dev) return
      this.$confirm('确定删除这条记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        var post_url = get_url(this.$store.state.dev, '/book/delete/')
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
              _this.books.splice(index, 1)
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
    edit_book_button_clicked: function (index, id) {
      if (!this.check_login() && !this.$store.state.dev) return
      this.is_insert = false
      this.dialog_title = '修改条目'
      this.insert_book_form.id = id
      this.insert_book_form.title = this.books[index].title
      this.insert_book_form.author = this.books[index].author
      this.insert_book_form.rate = this.books[index].rate
      this.insert_book_form.comment = this.books[index].comment
      this.insert_book_form_visible = true
    },
    insert_book_confirm_button_clicked: function () {
      if (!this.check_login() && !this.$store.state.dev) return
      var form_data = new FormData()
      form_data.append('id', this.insert_book_form.id)
      form_data.append('title', this.insert_book_form.title)
      form_data.append('author', this.insert_book_form.author)
      form_data.append('rate', this.insert_book_form.rate)
      form_data.append('comment', this.insert_book_form.comment)
      var file = document.getElementById('file').files[0]
      form_data.append('file', file)
      form_data.append('name', file.name)
      var post_url
      if (this.is_insert) {
        post_url = get_url(this.$store.state.dev, '/book/insert/')
      } else post_url = get_url(this.$store.state.dev, '/book/modify/')
      var _this = this
      $.ajax({
        url: post_url,
        type: 'POST',
        data: form_data,
        contentType: false,
        processData: false,
        success: function (data) {
          data = JSON.parse(data)
          var code = data['code']
          if (code === 0) {
            _this.$message({
              showClose: true,
              type: 'success',
              message: '操作成功'
            })
            _this.$router.go(0)
          } else if (code === 1) {
            _this.$message({
              showClose: true,
              type: 'error',
              message: '操作失败'
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
    var post_url = get_url(this.$store.state.dev, '/book/id_list/')
    var _this = this
    $.ajax({
      ContentType: 'application/json; charset=utf-8',
      dataType: 'json',
      url: post_url,
      type: 'POST',
      success: function (data) {
        var id_list = data['id_list']
        console.log(data)
        if (id_list.length !== 0) {
          post_url = get_url(_this.$store.state.dev, '/book/info_list/')
          var post_data = { id_list: JSON.stringify(id_list) }
          $.ajax({
            ContentType: 'application/json; charset=utf-8',
            dataType: 'json',
            url: post_url,
            type: 'POST',
            data: post_data,
            success: function (data) {
              var info_list = data['info_list']
              console.log(info_list)
              for (var i = 0; i < info_list.length; i++) {
                var temp = {}
                temp.id = id_list[i]
                temp.title = info_list[i].title
                temp.author = info_list[i].author
                // temp.rate = String(info_list[i].rate).substr(0, 3)
                temp.rate = info_list[i].rate
                temp.rate_disabled = (info_list[i].rate !== 0)
                temp.time = info_list[i].post_time
                temp.comment = info_list[i].comment
                temp.img = info_list[i].img
                _this.books.push(temp)
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

<style type="text/css" scoped>
  .title{
    color: #303133;
    font-size: 24px;
  }
  .comment{
    padding: 0px 0px 0px 0px;
    color: #303133;
    font-size: 18px;
  }
  .time{
    font-size: 14px;
    float: right;
    padding-bottom: 10px;
    color: #909399;
  }
  .image{
    height: 200px;
    width: 200px;
    padding: 0px 0px 0px 0px;
    margin: 0px 0px 0px 0px;
  }
  .comment_container{
    height:70px;
  }
  .button{
    font-size: 20px;
    padding: 0px 0px 0px 0px;
  }
  .author{
    color: #606266;
  }
</style>