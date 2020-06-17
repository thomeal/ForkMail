<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-top">
        <div class="operations">
          {{time()}}
          <span @click="showUserInfo=true">{{user}}</span>
        </div>
        <el-button size="mini" @click="$router.push({path: '/'})">
          <i class="el-icon-switch-button"></i> 退出
        </el-button>
      </div>
      <div class="header-bottom">
        <div class="operations">
          <el-select v-model="selectedMailBox" placeholder="请选择邮箱" size="mini">
            <el-option
              v-for="mail in mails"
              :key="mail"
              :label="mail"
              :value="mail">
            </el-option>
          </el-select>
          <el-button icon="el-icon-refresh" size="mini" @click="getMailList"></el-button>
          <el-button-group>
            <el-button icon="el-icon-chat-line-square" size="mini"></el-button>
            <el-button icon="el-icon-delete" size="mini" @click="deleteMail"></el-button>
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
      <div :class="{'mailPreview':true,'selectedPreview':mail.chosen}" v-for="(mail) in search===''?rawMail:filtered"
           :key="mail.id"
           @click="chooseMail(mail)">
        <div class="context">
          <div class="head">
            <div class="sender">
              {{showSender(mail.sender)}}
            </div>
            <div class="time">
              {{mail.date.toLocaleDateString()}}
            </div>
          </div>
          <div class="subject">{{mail.subject}}</div>
          <div class="content">{{mail.extracted}}</div>
        </div>
      </div>
    </div>
    <div class="detail">
      <div class="header">
        <div style="position: relative">
          <el-tooltip effect="dark" :content="selectedMail.sender.email" placement="top">
            <div class="sender">
              {{selectedMail.sender.name?selectedMail.sender.name:selectedMail.sender.email}}
            </div>
          </el-tooltip>
          <div class="time">
            <span style="margin-right: 5px">
              {{selectedMail.date.toLocaleDateString([], {year: 'numeric', month: 'long', day: 'numeric'})}}
            </span>
            <span>
              {{selectedMail.date.toLocaleTimeString()}}
            </span>
          </div>
        </div>
        <div style="margin: 5px 0;">
          <div class="common">
            {{selectedMail.subject}}
          </div>
        </div>
        <div>
          <div class="common">
            <span>收件人:</span>
            <el-tooltip effect="dark" :content="selectedMail.receiver.email" placement="top">
              <div class="infoBlock">
                {{selectedMail.receiver.name?selectedMail.receiver.name:selectedMail.receiver.email}}
              </div>
            </el-tooltip>
          </div>
        </div>
      </div>
      <div class="content" v-if="selectedMail.html!==''||selectedMail.plain.match(/<[^>]*>/)"
           v-html="selectedMail.html!==''?selectedMail.html:selectedMail.plain"></div>
      <div class="content" v-else v-text="selectedMail.plain"></div>
    </div>
    <user-info :mails="mails" :enabled="showUserInfo" @close="showUserInfo=false"></user-info>
  </div>
</template>

<script>
  import UserInfo from "./userInfo/userInfo";
  import {Loading} from 'element-ui';

  export default {
    name: "mail",
    components: {UserInfo},
    data() {
      return {
        showUserInfo: false,
        user: '',
        search: '',
        selectedMailBox: '',
        selectedMail: {},
        mails: [],
        rawMail: [],
        detail: '',
        filtered: [],
        reply: ''
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
      chooseMail(mail) {
        this.selectedMail.chosen = false;
        mail['chosen'] = true;
        this.selectedMail = mail;
      },
      getMailList() {
        let loadingInstance = Loading.service({fullscreen: true});
        this.$axios({
          url: 'http://localhost:8000/getAllMails/?token='
            + localStorage['token'] + '&mail=\'' + this.selectedMailBox + '\'',
          method: 'GET',
        }).then(res => {
          loadingInstance.close();
          if (res.data.success) {
            this.rawMail = res.data.mail.reverse().map(item => {
              item.sender = eval(item.sender)[0];
              item.receiver = eval(item.receiver)[0];
              item.plain = unescape(item.plain.replace(/<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)>|\\*(?=[\u4e00-\u9fa5|\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5])/g, '').replace(/\\/g, '%'));
              item.html = unescape(item.html.replace(/<![ \r\n\t]*(--([^\-]|[\r\n]|-[^\-])*--[ \r\n\t]*)>|\\*(?=[\u4e00-\u9fa5|\u3002|\uff1f|\uff01|\uff0c|\u3001|\uff1b|\uff1a|\u201c|\u201d|\u2018|\u2019|\uff08|\uff09|\u300a|\u300b|\u3008|\u3009|\u3010|\u3011|\u300e|\u300f|\u300c|\u300d|\ufe43|\ufe44|\u3014|\u3015|\u2026|\u2014|\uff5e|\ufe4f|\uffe5])/g, '').replace(/\\/g, '%'));
              if (item.plain !== "")
                item['extracted'] = item.plain.replace(/<style(([\s\S])*?)<\/style>|<script(([\s\S])*?)<\/script>|&[^;]*;|(?:^|\n|\r)\s*\/\*[\s\S]*?\*\/\s*(?:\r|\n|$)|<[^>]*>|\\r|\\t|\\n|-*/g, "");
              else
                item['extracted'] = item.html.replace(/<style(([\s\S])*?)<\/style>|<script(([\s\S])*?)<\/script>|&[^;]*;|(?:^|\n|\r)\s*\/\*[\s\S]*?\*\/\s*(?:\r|\n|$)|<[^>]*>|\\r|\\t|\\n|-*/g, "");
              item['date'] = new Date(item.date);
              item['chosen'] = false;
              return item;
            });
            this.rawMail[0]['chosen'] = true;
            this.selectedMail = this.rawMail[0];
          } else {
            this.$message.error(res.data.message);
            if (res.data['reLoginRequired']) {
              localStorage.removeItem('token');
              this.$router({path: '/'});
            }
          }
        }).catch(e => {
          loadingInstance.close();
          this.$message.error('服务器开小差了');
        })
      },
      deleteMail() {
        this.$axios({
          url: 'http://localhost:8000/deleteMail/',
          method: 'POST',
          data: {
            id: this.selectedMail.id,
            token: localStorage['token'],
            mail: '\'' + this.selectedMailBox + '\''
          }
        }).then(res => {
          if (res.data.success) {
            this.$message.success(res.data.message);
            let index = this.rawMail.findIndex(item => item.id === this.selectedMail.id);
            this.selectedMail['chosen'] = false;
            this.rawMail.splice(index, 1);
            this.rawMail[index - 1 > -1 ? index - 1 : 0]['chosen'] = true;
            this.selectedMail = this.rawMail[index - 1 > -1 ? index - 1 : 0];
          } else {
            this.$message.error(res.data.message);
          }
        }).catch(e => {
          this.$message.error('服务器开小差了');
        })
      }
    },
    watch: {
      search: {
        handler() {
          this.filtered = this.rawMail.filter(mail => mail.extracted.includes(this.search))
        },
        deep: true,
        immediate: true
      }
    },
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
          this.selectedMailBox = this.mails[0];
          this.getMailList();
        }
      }).catch(e => {
        this.$message.error('服务器开小差了');
        this.$router({path: '/'});
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

    > .header {
      grid-area: header;
      background: linear-gradient(180deg, rgba(227, 227, 227, 0.9), rgba(200, 200, 200, 1));
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

          span {
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
      cursor: default;

      .mailPreview {
        .context {
          margin-left: 20px;
          border-bottom: rgba(230, 230, 230, 1.000) 1px solid;
          padding: 5px 5px 5px 5px;
          font-size: 14px;

          .head {
            height: 20px;
            position: relative;

            .sender {
              color: rgba(45, 45, 45, 1.000);
              overflow: hidden;
              font: {
                weight: bold;
              };
              display: inline-block;
            }

            .time {
              display: inline-block;
              position: absolute;
              color: rgba(128, 128, 128, 1.000);
              right: 5px;
            }
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

      .selectedPreview {
        background: rgba(0, 100, 224, 1.000);

        .context {
          border-bottom: rgba(0, 100, 224, 1.000) 1px solid;

          .head {
            .sender {
              color: rgba(255, 255, 255, 1.000);
            }

            .time {
              color: rgba(255, 255, 255, 1.000);
            }
          }

          .subject {
            color: rgba(255, 255, 255, 1.000);
          }

          .content {
            color: rgba(139, 177, 241, 1.000);
          }
        }
      }
    }

    .detail {
      grid-area: detail;
      background: #ffffff;
      padding: 10px 40px;
      height: 100%;
      overflow: hidden;

      > .header {
        height: 80px;
        position: relative;
        overflow: hidden;
        color: rgba(40, 39, 40, 1.000);
        border-bottom: rgba(230, 230, 230, 1.000) 1px solid;
        padding-bottom: 10px;

        .selectedBlock {
          background: rgba(2, 122, 255, 1.000);
          color: rgba(220, 235, 255, 1.000);
        }

        .sender {
          padding: 0 5px;
          display: inline-block;
          font-weight: bold;

          &:hover {
            background: rgba(187, 215, 255, 1.000);
          }
        }

        .common {
          display: inline-block;
          padding: 0 5px;
        }

        .infoBlock {
          display: inline-block;
          color: rgba(128, 128, 128, 1.000);

          &:hover {
            background: rgba(187, 215, 255, 1.000);
            color: rgba(0, 0, 0, 1.000);
          }
        }

        .time {
          right: 0;
          position: absolute;
          display: inline-block;
          color: rgba(128, 128, 128, 1.000);
        }
      }

      .content {
        padding: 10px 0;
        width: 100%;
        height: 100%;
        overflow: scroll;
      }
    }


  }

</style>
