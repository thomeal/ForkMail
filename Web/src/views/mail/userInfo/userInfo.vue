<template>
  <el-dialog id="userInfo" title="个人信息" :visible="visible" width="40%" @close="$emit('close')">
    <div class="accountInfo">
      <div class="strongTitle">
        账户信息
      </div>
      <div class="infoBlock">
        <div class="infoLine">
          <span class="infoBlack">昵称: </span>
          <span class="infoGray"> {{nickname}}</span>
        </div>
        <div class="infoLine">
          <span class="infoBlack">手机号: </span>
          <span class="infoGray"> {{mobile}}</span>
        </div>
      </div>
      <div class="strongTitle">
        邮箱信息
      </div>
      <div class="infoBlock">
        <div class="infoLine" v-for="(mail,index) in mails" :key="index">
          <span class="infoBlack">{{mail}}</span>
          <i class="el-icon-edit"/>
          <i class="el-icon-delete"/>
        </div>
        <div class="infoLine">
          <el-button icon="el-icon-plus" size="mini">添加邮箱</el-button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script>
  export default {
    name: "userInfo",
    props: {
      enabled: Boolean,
      mails: Array
    },
    data() {
      return {
        mobile: '',
        nickname: '',
      }
    },
    methods: {},
    computed: {
      visible() {
        return this.enabled;
      }
    },
    beforeMount() {
      this.nickname = localStorage['nickname'];
      this.mobile = localStorage['mobile'];
    }
  }
</script>

<style lang="scss">
  #userInfo {
    .el-dialog__body {
      padding: 0;
    }
  }
</style>

<style lang="scss" scoped>
  .accountInfo {
    max-height: 500px;
    padding: 0 20px 10px;
    overflow: hidden;
    border: {
      top: rgba(214, 214, 214, 1.000) 1px solid;
      bottom: rgba(214, 214, 214, 1.000) 1px solid;
    }

    .strongTitle {
      margin-top: 10px;
      color: rgba(39, 62, 82, 1.000);
      font-weight: bold;
    }

    .infoBlack {
      color: rgba(39, 62, 82, 1.000);
    }

    .infoGray {
      color: rgba(128, 128, 128, 1.000);
    }

    .infoBlock {
      display: block;
      min-height: 50px;
      max-height: 200px;
      overflow: scroll;
      border: {
        top: rgba(214, 214, 214, 1.000) 1px solid;
        bottom: rgba(214, 214, 214, 1.000) 1px solid;
      }

      .infoLine {
        display: block;
        margin: 5px 5px;

        .el-icon-edit {
          margin: 0 5px;

          &:hover {
            color: rgba(2, 122, 255, 1.000);
          }
        }

        .el-icon-delete {
          margin: 0 5px;

          &:hover {
            color: #d21b1b;
          }
        }
      }
    }
  }

</style>
