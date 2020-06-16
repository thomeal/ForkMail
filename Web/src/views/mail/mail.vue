<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-top">
        <div class="operations">
          {{time()}}
          <a @click="showUserInfo=true">{{user}}</a>
        </div>
        <el-button size="mini" @click="$router.push({path: '/'})" v-loading.fullscreen.lock="loading">
          <i class="el-icon-switch-button"></i> 退出
        </el-button>
      </div>
      <div class="header-bottom">
        <div class="operations">
          <el-select v-model="selectedMail" placeholder="请选择邮箱" size="mini">
            <el-option
              v-for="mail in mails"
              :key="mail"
              :label="mail"
              :value="mail">
            </el-option>
          </el-select>
          <el-button icon="el-icon-refresh" size="mini"></el-button>
          <el-button-group>
            <el-button icon="el-icon-chat-line-square" size="mini"></el-button>
            <el-button icon="el-icon-delete" size="mini"></el-button>
          </el-button-group>
          <el-button icon="el-icon-edit" size="mini"></el-button>
        </div>
        <el-input
          placeholder="搜索"
          prefix-icon="el-icon-search"
          size="mini"
          v-model="search">
        </el-input>
      </div>
    </div>
    <div class="mailList">
      <div class="mailPreview" v-for="(mail,index) in rawMail" :key="index">
        <div class="context">
          <div class="sender">{{showSender(mail.sender)}}</div>
          <div class="subject">{{mail.subject}}</div>
          <div class="content">{{mail.extracted}}</div>
        </div>
      </div>
    </div>
    <div class="detail">

    </div>
    <user-info :enabled="showUserInfo" @close="showUserInfo=false"></user-info>
  </div>
</template>

<script>
  import UserInfo from "./userInfo/userInfo";

  export default {
    name: "mail",
    components: {UserInfo},
    data() {
      return {
        loading: false,
        showUserInfo: false,
        user: '',
        search: '',
        selectedMail: '',
        mails: [],
        rawMail: []
      }
    },
    methods: {
      time() {
        let hour = new Date().getHours()
        if (hour < 5) return '晚上好'
        if (hour < 12) return '上午好,'
        if (hour < 18) return '下午好,'
        return '晚上好,'
      },
      showSender(sender) {
        if (sender.name)
          return sender.name;
        return sender.email;
      },
      getMailList() {
        this.loading = true;
        this.$axios({
          url: 'http://localhost:8000/getAllMails/?token='
            + localStorage['token'] + '&mail=\'' + this.selectedMail + '\'',
          method: 'GET',
        }).then(res => {
          this.loading = false;
          if (res.data.success) {
            this.rawMail = res.data.mail.reverse().map(item => {
              item.sender = eval(item.sender)[0];
              item.plain = item.plain.replace(/<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)>|\\*(?=[\u4e00-\u9fa5|\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5])/g, '');
              item.html = item.html.replace(/<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)>|\\*(?=[\u4e00-\u9fa5|\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5])/g, '');
              if (item.plain !== "")
                item['extracted'] = item.plain.replace(/<style(([\s\S])*?)<\/style>|<script(([\s\S])*?)<\/script>|&[^;]*;|(?:^|\n|\r)\s*\/\*[\s\S]*?\*\/\s*(?:\r|\n|$)/g, "").replace(/<[^>]*>/g, "").replace(/\\r|\\t|\\n|-*/g, '');
              else
                item['extracted'] = item.html.replace(/<style(([\s\S])*?)<\/style>|<script(([\s\S])*?)<\/script>|&[^;]*;|(?:^|\n|\r)\s*\/\*[\s\S]*?\*\/\s*(?:\r|\n|$)/g, "").replace(/<[^>]*>/g, "").replace(/\\r|\\t|\\n|-*/g, '');
              return item;
            });
          } else {
            this.$message.error(res.data.message);
            if (res.data['reLoginRequired']) {
              localStorage.removeItem('token');
              this.$router({path: '/'});
            }
          }
        }).catch(e => {
          this.loading = false;
          this.$message.error('服务器开小差了');
        })
      }
    },
    computed: {},
    beforeMount() {
      this.user = localStorage['nickname'];
      this.$axios({
        url: 'http://localhost:8000/getMailBoxes',
        method: 'GET',
        params: {
          token: localStorage['token']
        }
      }).then(res => {
        if (!res.data.success) {
          this.$message.error(res.data.message);
          if (res.data['reLoginRequired']) {
            localStorage.removeItem('token');
            this.$router({path: '/'});
          }
        } else {
          this.mails = res.data.mailBoxes;
          this.selectedMail = this.mails[0];
          this.getMailList();
        }
      }).catch(e => {
        this.$message.error('服务器开小差了');
      })
    }
  }
</script>

<style lang="scss" scoped>
  .el-button, .el-input, .el-select {
    border: #c3c3c3 1px solid;
    border-radius: 5px;
  }

  .wrapper {
    background-image: url("../../assets/1.jpg");
    background-size: cover;
    height: 100%;
    width: 100%;
    display: grid;
    grid-template-areas:
      'header header'
      'mailList detail';
    grid-template-rows: 70px;
    grid-template-columns: 350px;

    .header {
      grid-area: header;
      background: linear-gradient(180deg, rgb(227, 227, 227), rgb(200, 200, 200));
      display: grid;
      grid-template-areas:
        'header-top'
        'header-bottom';
      grid-template-rows: 40px 30px;
      border-bottom: #a5a5a5 1px solid;

      .header-top {
        grid-area: header-top;
        position: relative;

        > .el-button {
          position: absolute;
          top: 5px;
          right: 10px;
        }

        > .operations {
          position: absolute;
          top: 5px;
          left: 12px;
          color: rgba(85, 85, 85, 1.000);
          font: {
            family: "PingFang SC", monospace;
            size: 17px;
          }

          a {
            &:hover {
              color: rgba(0, 98, 225, 1.000);
              cursor: pointer;
            }
          }
        }
      }

      .header-bottom {
        grid-area: header-bottom;
        position: relative;

        > .el-input {
          width: 300px;
          position: absolute;
          border-radius: 5px;
          top: -3px;
          right: 10px;
        }

        > .operations {
          position: absolute;
          top: -3px;
          left: 10px;

          > .el-button-group {
            margin-top: -1px;
          }
        }
      }
    }

    .mailList {
      grid-area: mailList;
      background: #ffffff;
      border-right: #d5d5d5 1px solid;
      overflow: scroll;

      .mailPreview {
        .context {
          margin-left: 20px;
          border-bottom: rgba(230, 230, 230, 1.000) 1px solid;
          padding: 5px 5px 5px 5px;
          font-size: 14px;

          .sender {
            color: rgba(45, 45, 45, 1.000);
            overflow: hidden;
            height: 20px;
            font: {
              weight: bold;
            };
          }

          .subject {
            color: rgba(39, 39, 39, 1.000);
            overflow: hidden;
            height: 20px;
          }

          .content {
            color: rgba(128, 128, 128, 1.000);
            overflow: hidden;
            height: 40px;
          }
        }
      }
    }

    .detail {
      grid-area: detail;
      background: #ffffff;
    }


  }

</style>
