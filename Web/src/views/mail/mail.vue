<template>
  <div class="wrapper">
    <div class="header">
      <div class="header-top">
        <div class="operations">
          {{time()}}
          <a @click="showUserInfo=true">{{user}}</a>
        </div>
        <el-button size="mini"><i class="el-icon-switch-button"></i> 退出</el-button>
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
        showUserInfo: false,
        user: '',
        search: '',
        selectedMail: '',
        mails: ['111111@qq.com', '222222@qq.com', '3333333@qq.com', '4444444@qq.com']
      }
    },
    methods: {
      time() {
        let hour = new Date().getHours()
        if (hour < 12) return '上午好,'
        if (hour < 18) return '下午好,'
        return '晚上好,'
      }
    },
    beforeMount() {
      this.user = localStorage['nickname'];
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
    }

    .detail {
      grid-area: detail;
      background: #ffffff;
    }


  }

</style>
