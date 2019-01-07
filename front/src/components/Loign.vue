<template>
    <div id="login">
        <el-form :model="loginForm" :rules="loginRules" ref="loginForm" label-width="80px">
            <el-form-item label="用户名" prop="username">
               <el-input v-model="loginForm.username" placeholder="请输入用户名/手机号"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
               <el-input v-model="loginForm.password" placeholder="请输入密码" auto-complete="on"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">登录</el-button>
                <el-button>取消</el-button>
            </el-form-item>
        </el-form>
        

        
    </div>
</template>


<script>
import {loginReq} from '@/apis/Login'

export default {
    name:"#login",
    data() {
        return {
            loginForm:{
                username:'',
                password:'',
            },
            loginRules:{
                username:[
                    {
                        required:true,
                        message:"请输入用户名",
                        trigger:'blur'
                    }
                ],
                password:[
                    {
                        required:true,
                        message:'请输入密码',
                        trigger:'blur'
                    }
                ]
            }

        }
    },
    methods: {
        handleLogin (){
           this.$refs.loginForm.validate((valid) => {
               if(valid){
                  loginReq(this.loginForm.username,this.loginForm.password).then((res) => {
                      console.log(res.data.status);
                  })
               }else{
                   this.$message.error("用户名或密码错误");
               }
           })
      }
    }
    
}
</script>

<style lang="scss" scoped>
.el-input{
    width: 300px;
}



</style>
