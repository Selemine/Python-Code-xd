<template>
  <form @submit.prevent>
    <div class="register">
      <div class="container">
        <div class="register__wrapper">
          <div>
            <img
              src="@/assets/images/Logo.svg"
              class="register__logo"
              alt="logo"
            />
          </div>
          <h1 class="register__title">Create an account</h1>
          <p class="register__error-message" v-show="error && isVisibleError">
            {{ errorMessage }}
          </p>
          <hr class="register__line-error" v-show="error && isVisibleError" />
          <div class="register__user-name">
            <input
              type="text"
              placeholder="Username"
              class="register__input"
              v-model.trim="userName.name"
              :class="{ 'error-validate': v$.userName.name.$error }"
            />
            <p
              class="register__error-input"
              v-if="
                v$.userName.name.$error &&
                v$.userName.name.$errors[0].$params.type === 'required'
              "
            >
              Имя пользователя не должо быть пустым
            </p>
            <p
              class="register__error-input"
              v-if="
                v$.userName.name.$error &&
                v$.userName.name.$errors[0].$params.type === 'minLength'
              "
            >
              Минимальная длина имени {{ userName.minLengthName }} символов.
              Сейчас он {{ userName.name.length }}
            </p>
          </div>
          <div class="register__email">
            <input
              type="text"
              placeholder="Enter your email address"
              class="register__input"
              v-model.trim="email"
              :class="{
                'error-validate': v$.email.$error,
              }"
            />
            <p
              class="register__error-input"
              v-if="
                v$.email.$error &&
                v$.email.$errors[0].$params.type === 'required'
              "
            >
              Поле Email не должно быть пустым
            </p>
            <p
              class="register__error-input"
              v-if="
                v$.email.$error && v$.email.$errors[0].$params.type === 'email'
              "
            >
              Введите корректный Email адрес
            </p>
          </div>
          <div class="register__paswd">
            <input
              type="text"
              placeholder="Password"
              class="register__input"
              v-model.trim="login.password"
              :class="{
                'error-validate': v$.login.password.$error,
              }"
            />
            <p
              class="register__error-input"
              v-if="
                v$.login.password.$error &&
                v$.login.password.$errors[0].$params.type === 'required'
              "
            >
              Поле Password не должно быть пустым
            </p>
            <p
              class="register__error-input"
              v-if="
                v$.login.password.$error &&
                v$.login.password.$errors[0].$params.type === 'minLength'
              "
            >
              Минимальная длина пароля {{ login.minLengthPaswd }} символов.
              Сейчас он {{ login.password.length }}
            </p>
          </div>
          <div class="register__conf-paswd">
            <input
              type="text"
              placeholder="Confirm Password"
              class="register__input"
              v-model.trim="login.confirm"
              :class="{
                'error-validate': v$.login.confirm.$error,
              }"
            />
            <p
              class="register__error-input"
              v-if="
                v$.login.confirm.$error &&
                v$.login.confirm.$errors[0].$params.type === 'required'
              "
            >
              Повторите пароль
            </p>
            <p
              class="register__error-input"
              v-if="
                v$.login.confirm.$error &&
                v$.login.confirm.$errors[0].$params.type === 'sameAs'
              "
            >
              Пароли не совпадают
            </p>
          </div>
        </div>

        <button
          class="register__btn-create"
          type="submit"
          @click="createHendel"
        >
          Create an account
        </button>

        <div class="login-element">
          <div class="line"></div>
          <p class="login-element__txt">Or register with</p>
          <div class="line"></div>
        </div>

        <div class="register__alternative">
          <button class="register__alternative-google">
            <div>
              <img src="@/assets/images/icons/google.svg" alt="icon-google" />
            </div>
            <p class="register__alternative-google-txt">Continue with Google</p>
          </button>
          <button class="register__alternative-facebook">
            <div>
              <img
                src="@/assets/images/icons/facebook.svg"
                alt="icon-facebook"
              />
            </div>
            <p class="register__alternative-facebook-txt">
              Continue with Facebook
            </p>
          </button>
        </div>

        <div class="register__sign-up">
          <h3 class="register__sign-txt">Already have an account?</h3>
          <button class="register__sign-btn" @click="$router.push('/')">
            Login
          </button>
        </div>
      </div>
    </div>
  </form>
</template>
<script>
import useValidate from "@vuelidate/core";
import { required, email, minLength, sameAs } from "@vuelidate/validators";
import { errorMessage } from "@/layout/errorMessage";

export default {
  name: "register",
  data() {
    return {
      v$: useValidate(),
      userName: {
        name: "",
        minLengthName: 2,
      },
      email: "",
      login: {
        password: "",
        confirm: "",
        minLengthPaswd: 8,
      },
      isVisibleError: false,
    };
  },
  validations() {
    const minLengthPassword = this.login.minLengthPaswd;
    const minLengthNames = this.userName.minLengthName;
    return {
      userName: {
        name: { required, minLength: minLength(minLengthNames) },
      },
      email: { required, email },
      login: {
        password: { required, minLength: minLength(minLengthPassword) },
        confirm: { required, sameAs: sameAs(this.login.password) },
      },
    };
  },
  methods: {
    async createHendel() {
      this.v$.$validate(); // checks all inputs
      if (this.v$.$error) {
        return;
      } else {
        const formData = {
          name: this.userName.name,
          email: this.email,
          password: this.login.password,
        };

        try {
          await this.$store.dispatch("register", formData);
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
.register {
  padding: 0px 10px;
  &__wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  &__logo {
    margin: 25px 0;
  }
  &__title {
    margin-bottom: 30px;
    font-weight: 500;
    font-size: 20px;
    line-height: 16px;
    color: #3d3d3d;
  }
  &__input {
    margin: 10px 0px;
    width: 358px;
    height: 50px;
    border: 1px solid #eaeaea;
    border-radius: 10px;
    padding: 16px 0px 16px 16px;
  }
  &__btn-create {
    margin-top: 25px;
    padding: 22px 110px;
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
    margin: 0px 0px 2px 10px;
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

.login__input::placeholder {
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
