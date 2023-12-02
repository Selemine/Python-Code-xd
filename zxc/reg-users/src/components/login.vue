<template>
  <form @submit.prevent>
    <div class="login">
      <div class="container">
        <div class="login__wrapepr">
          <div class="login__logo">
            <img src="@/assets/images/Logo.svg" alt="logo" />
          </div>
          <h1 class="login__title">Login</h1>
          <p class="login__error-message" v-show="error && isVisibleError">
            {{ errorMessage }}
          </p>
          <hr class="login__line-error" v-show="error && isVisibleError" />
          <div class="login__user-name">
            <input
              type="text"
              placeholder="almamun_uxui@outlook.com"
              class="login__input-login"
              v-model.trim="email"
              :class="{
                'error-validate': v$.email.$error,
              }"
            />
            <p
              class="login__error-input"
              v-if="
                v$.email.$error &&
                v$.email.$errors[0].$params.type === 'required'
              "
            >
              Поле Email не должно быть пустым
            </p>
            <p
              class="login__error-input"
              v-if="
                v$.email.$error && v$.email.$errors[0].$params.type === 'email'
              "
            >
              Введите корректный Email адрес
            </p>
          </div>
          <div class="login__user-paswd">
            <input
              type="text"
              placeholder="password"
              class="login__input-login"
              v-model.trim="login.password"
              :class="{
                'error-validate': v$.login.password.$error,
              }"
            />
            <p
              class="login__error-input"
              v-if="
                v$.login.password.$error &&
                v$.login.password.$errors[0].$params.type === 'required'
              "
            >
              Поле Password не должно быть пустым
            </p>
            <p
              class="login__error-input"
              v-if="
                v$.login.password.$error &&
                v$.login.password.$errors[0].$params.type === 'minLength'
              "
            >
              Минимальная длина пароля {{ login.minLengthPaswd }} символов.
              Сейчас он {{ login.password.length }}
            </p>
          </div>
          <button class="login__forgot-paswd">Forgot Password?</button>
        </div>

        <button class="login__btn" type="submit" @click="submitHendel">
          Login
        </button>

        <div class="login-element">
          <div class="line"></div>
          <p class="login-element__txt">Or login with</p>
          <div class="line"></div>
        </div>

        <div class="login__alternative">
          <button class="login__alternative-google">
            <div>
              <img src="@/assets/images/icons/google.svg" alt="icon-google" />
            </div>
            <p class="login__alternative-google-txt">Login with Google</p>
          </button>
          <button class="login__alternative-facebook">
            <div>
              <img
                src="@/assets/images/icons/facebook.svg"
                alt="icon-facebook"
              />
            </div>
            <p class="login__alternative-facebook-txt">Login with Facebook</p>
          </button>
        </div>
        <div class="login__sign-up">
          <h3 class="login__sign-txt">Don’t have an account?</h3>
          <button class="login__sign-btn" @click="$router.push('register')">
            Sign Up
          </button>
        </div>
      </div>
    </div>
  </form>
</template>
<script>
import { errorMessage } from "@/layout/errorMessage";
import useValidate from "@vuelidate/core";
import { required, email, minLength } from "@vuelidate/validators";

export default {
  name: "login",
  data() {
    return {
      v$: useValidate(),
      email: "",
      login: {
        password: "",
        minLengthPaswd: 8,
      },
      isVisibleError: false,
    };
  },
  validations() {
    const minLengthPassword = this.login.minLengthPaswd;
    return {
      email: { required, email },
      login: {
        password: {
          required,
          minLength: minLength(minLengthPassword),
        },
      },
    };
  },
  methods: {
    async submitHendel() {
      this.v$.$validate(); // checks all inputs
      if (this.v$.$error) {
        return;
      } else {
        const formData = {
          email: this.email,
          password: this.login.password,
        };

        try {
          await this.$store.dispatch("login", formData);
          this.$router.push("/main");
        } catch (error) {}
      }
    },
    hideErrorMessage() {
      this.isVisibleError = false;
    },
  },
  computed: {
    error() {
      return this.$store.getters.error;
    },
    errorMessage() {
      return errorMessage(this.$store.getters.error);
    },
  },
  watch: {
    error(fbError) {
      console.log(fbError);
      this.isVisibleError = !!fbError;
      if (this.isVisibleError) {
        setTimeout(this.hideErrorMessage, 2500);
      }
    },
  },
};
</script>
<style lang="scss" scoped>
.container {
  max-width: 350px;
  margin: 0 auto;
}
.login {
  padding: 0px 10px;
  &__wrapepr {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  &__logo {
    margin: 40px 0;
  }
  &__title {
    margin-bottom: 30px;
    font-weight: 500;
    font-size: 20px;
    line-height: 16px;
    color: #3d3d3d;
  }
  &__user-paswd {
    margin: 20px 0px 12px 0px;
  }
  &__forgot-paswd {
    align-self: flex-end;
    font-weight: 400;
    font-size: 14px;
    line-height: 16px;
    color: #46a358;
  }
  &__input-login {
    width: 358px;
    height: 50px;
    border: 1px solid #eaeaea;
    border-radius: 10px;
    padding: 16px 0px 16px 16px;
  }
  &__btn {
    margin-top: 40px;
    padding: 22px 158px;
    font-weight: 700;
    font-size: 16px;
    line-height: 16px;
    color: #ffffff;
    width: 358px;
    height: 60px;
    background: #46a358;
    border-radius: 10px;
  }
  &__alternative-google {
    margin-bottom: 20px;
    display: flex;
    padding: 0px 0px 0px 100px;
    align-items: center;
    width: 358px;
    height: 50px;
    background: #4086f4;
    border-radius: 10px;
  }
  &__alternative-facebook {
    margin-bottom: 30px;
    display: flex;
    padding: 0px 0px 0px 100px;
    align-items: center;
    width: 358px;
    height: 50px;
    background: #3b5999;
    border-radius: 10px;
  }
  &__alternative-facebook-txt {
    font-weight: 500;
    margin-left: 10px;
    font-size: 15px;
    line-height: 16px;
    color: #ffffff;
  }
  &__alternative-google-txt {
    font-weight: 500;
    margin-left: 10px;
    font-size: 15px;
    line-height: 16px;
    color: #ffffff;
  }
  &__sign-up {
    max-width: 210px;
    margin: 0 auto;
    display: flex;
    font-weight: 400;
    font-size: 15px;
    line-height: 16px;
    color: #727272;
  }
  &__sign-txt {
    margin-right: 5px;
  }
  &__sign-btn {
    color: #46a358;
    font-weight: 700;
    font-size: 16px;
  }
  &__error-input {
    color: red;
    margin: 5px 0 0 10px;
  }
  &__line-error {
    margin: 5px 0 10px 0;
    height: 2px;
    width: 100%;
    background-color: red;
    animation: lineAnimation 2.55s linear;
  }
  &__error-message {
    text-align: center;
    margin-top: 10px;
    color: red;
    font-size: 16px;
  }
}

.login__input-login::placeholder {
  font-weight: 400;
  font-size: 14px;
  line-height: 16px;
  color: #a5a5a5;
}
.login-element {
  display: flex;
  align-items: center;
  &__txt {
    margin: 0px 10px;
    font-weight: 400;
    font-size: 13px;
    line-height: 15px;
    color: #3d3d3d;
  }
}

.line {
  flex-grow: 1;
  border: 1px solid #eaeaea;
}

.login-element span {
  padding: 0 10px;
}

.login-element {
  margin: 30px 0;
}
input:focus {
  border: 1px solid #46a358;
}
.error-validate:focus {
  border: 1px solid red;
}
.error-validate {
  border: 1px solid red;
}

@keyframes lineAnimation {
  0% {
    width: 100%;
  }
  100% {
    width: 0;
  }
}
</style>
