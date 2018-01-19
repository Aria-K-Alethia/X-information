<template>
  <div>
    <Header></Header>
    <div v-loading="loading" element-loading-text="你没有权限访问本页，请先登录" class="main_container">
      <el-tabs tab-position="left">
        <el-tab-pane label="消息来源统计报表">
            <el-row class="term">
              <el-col :span="3" class="date">
                <span class="head">选择日期</span>
              </el-col>
              <el-col :span="8">
                <el-date-picker v-model="noti_date" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" unlink-panels align="right" :picker-options="noti_picker_options" format="yyyy-MM-dd">
                </el-date-picker>
              </el-col>
              <el-col :span="4">
                <el-button type="primary" @click="noti_date_confirm_button_clicked">
                  确定
                </el-button>
              </el-col>
            </el-row>
            <el-row>
            <hr width="100%" class="term_hr"/>
          </el-row>
            <el-row class="term">
              <el-row class="head">
                <span class="head">总消息条数统计表</span>
              </el-row>
              <el-row>
                <el-col>
                  <el-table :data="noti_from_total_data" show-summary>
                    <el-table-column prop="from" label="消息来源">
                    </el-table-column>
                    <el-table-column prop="total" label="总量">
                    </el-table-column>
                  </el-table>
                </el-col>
              </el-row>
            </el-row>
            <el-row>
            <hr width="100%" class="term_hr"/>
          </el-row>
            <el-row class="term">
              <el-row class="head">
                <span class="head">消息量折线图</span>
              </el-row>
              <el-row class="charts">
                <div id="noti_line_chart" :style="{width: '1000px', height: '500px'}"></div>
              </el-row>
            </el-row>
        </el-tab-pane>
        <el-tab-pane label="年度读书量统计图">
            <el-row class="term">
              <el-col :span="3" class="date">
                <span class="head">选择日期</span>
              </el-col>
              <el-col :span="8">
                <el-date-picker v-model="book_date" type="daterange" range-separator="至" start-placeholder="开始日期" end-placeholder="结束日期" unlink-panels align="right" :picker-options="noti_picker_options" format="yyyy-MM-dd" disabled>
                </el-date-picker>
              </el-col>
              <el-col :span="4">
                <el-button type="primary" @click="book_date_confirm_button_clicked">
                  确定
                </el-button>
              </el-col>
            </el-row>
          <el-row>
            <hr width="100%" class="term_hr"/>
          </el-row>
            <el-row class="term">
              <el-row class="head">
                <span class="head">历年读书量统计图</span>
              </el-row>
              <el-row class="charts">
                <div id="book_line_chart" :style="{width: '1000px', height: '300px'}"></div>
              </el-row>
            </el-row>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script type="text/javascript">
/* eslint-disable camelcase */
import Header from '../general/Header.vue'
import $ from 'jquery'
import get_url from '../general/getUrl.js'
export default {
  name: 'Graph',
  components: { Header },
  data () {
    return {
      loading: false,
      noti_date: '',
      book_date: '',
      noti_line_chart: '',
      book_line_chart: '',
      noti_from_total_data: [],
      noti_picker_options: {
        shortcuts: [{
          text: '最近一周',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一个月',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近三个月',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '最近一年',
          onClick (picker) {
            const end = new Date()
            const start = new Date()
            start.setTime(start.getTime() - 3600 * 1000 * 24 * 30 * 12)
            picker.$emit('pick', [start, end])
          }
        }]
      }
    }
  },
  methods: {
    noti_date_confirm_button_clicked: function () {
      if (!this.check_login() && !this.$store.state.dev) return
      if (this.noti_date === '') {
        this.$message({
          showClose: true,
          type: 'info',
          message: '请先指定时间跨度噢'
        })
        return
      }
      var post_url = get_url(this.$store.state.dev, '/notification/per_month/')
      var from_time = [this.noti_date[0].getFullYear(), this.noti_date[0].getMonth() + 1].join('-')
      var end_time = [this.noti_date[1].getFullYear(), this.noti_date[1].getMonth() + 1].join('-')
      var post_data = { from_time: from_time, end_time: end_time }
      var _this = this
      $.ajax({
        ContentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: post_url,
        type: 'POST',
        data: post_data,
        success: function (data) {
          var data_list = data['data_list']
          var keys = data['keys']
          var legend = []
          var series = []
          for (var i = 0; i < data_list.length; i++) {
            legend.push(data_list[i].noti_from)
            var temp = {}
            temp.name = data_list[i].noti_from
            temp.type = 'line'
            temp.data = data_list[i].data
            series.push(temp)
          }
          var option = {
            title: {
              text: from_time + ' 至 ' + end_time + '的消息统计折线图'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: legend
            },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            toolbox: {
              feature: {
                saveAsImage: {}
              }
            },
            xAxis: {
              type: 'category',
              boundaryGap: false,
              data: keys
            },
            yAxis: {
              type: 'value'
            },
            series: series
          }
          _this.noti_line_chart.setOption(option)
        },
        error: function () {
          _this.$message({
            showClose: true,
            type: 'error',
            message: '无法连接服务器'
          })
        }
      })
      var post_url2 = get_url(this.$store.state.dev, '/notification/total/')
      var post_data2 = { from_time: from_time, end_time: end_time }
      $.ajax({
        ContentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: post_url2,
        type: 'POST',
        data: post_data2,
        success: function (data) {
          _this.noti_from_total_data = []
          var keys2 = data['keys']
          var data_list2 = data['data_list']
          for (var i = 0; i < keys2.length; i++) {
            var temp2 = {}
            temp2.from = keys2[i]
            temp2.total = data_list2[i]
            _this.noti_from_total_data.push(temp2)
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
    book_date_confirm_button_clicked: function () {
      if (!this.check_login() && !this.$store.state.dev) return
      this.$message({
        showClose: true,
        type: 'info',
        message: '选择日期功能暂未开放，目前会获得所有读书数量非0的年份'
      })
      var post_url = get_url(this.$store.state.dev, '/book/per_year/')
      var _this = this
      $.ajax({
        ContentType: 'application/json; charset=utf-8',
        dataType: 'json',
        url: post_url,
        type: 'POST',
        success: function (data) {
          var legend = ['读书量']
          var keys = data['keys']
          var data_list = data['data_list']
          var option = {
            title: {
              text: '年读书量统计折线图'
            },
            tooltip: {
              trigger: 'axis'
            },
            legend: {
              data: legend
            },
            grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
            },
            toolbox: {
              feature: {
                saveAsImage: {}
              }
            },
            xAxis: {
              type: 'category',
              boundaryGap: false,
              data: keys
            },
            yAxis: {
              type: 'value'
            },
            series: [
              {
                name: '读书量',
                type: 'line',
                data: data_list
              }
            ]
          }
          _this.book_line_chart.setOption(option)
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
    }
  },
  mounted: function () {
    /*
    if (!this.$store.state.is_login) {
      this.loading = true
      this.$router.push({ path: '/index' })
    }
    */
    this.noti_line_chart = this.$echarts.init(document.getElementById('noti_line_chart'))
    this.book_line_chart = this.$echarts.init(document.getElementById('book_line_chart'))
  }
}
</script>

<style type="text/css" scpoed>
  .term_hr{
    height:1px;
    border:none;
    border-top: 1px solid #E4E7ED;
    margin-top: 20px;
  }
  .main_container{
    font-family: Microsoft Yahei Light,Microsoft Yahei;
    margin-top: 50px;
  }
  .term{
    margin: 0px 0px 25px 25px;
  }
  .date{
    padding-top: 5px;
  }
  .head{
    color: #303133;
    font-size: 20px;
    margin-bottom: 10px;
  }
</style>