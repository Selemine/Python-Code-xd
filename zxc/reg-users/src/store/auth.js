import { initializeApp } from "firebase/app";
import { createUserWithEmailAndPassword, getAuth, signInWithEmailAndPassword } from "firebase/auth";
import { getDatabase, ref, set } from "firebase/database";
const firebaseConfig = {
	apiKey: "AIzaSyDxLwtBmMSNJ92HM3BdU3yyw_DDeblq86A",
  authDomain: "vue-register-e146c.firebaseapp.com",
  projectId: "vue-register-e146c",
  storageBucket: "vue-register-e146c.appspot.com",
  messagingSenderId: "679294892181",
  appId: "1:679294892181:web:4799c18212ccc65860439c",
  measurementId: "G-4HLV7D4H88"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const database = getDatabase(app);

export default {
  actions: {
    async login({ dispatch, commit }, { email, password }) {
      try {
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        await signInWithEmailAndPassword(auth, email, password);
      } catch (error) {
				commit('setError', error)
        throw error;
      }
    },
		async register({ dispatch, commit }, { email, password, name }) {
      try {
        await createUserWithEmailAndPassword(auth, email, password);
        const uid = await dispatch("getUid");
        const userRef = ref(database, `/users/${uid}/info`);
        await set(userRef, {
          name: name,
        });
      } catch (error) {
				commit('setError', error)
        throw error;
      }
    },
    getUid() {
      const user = auth.currentUser;
      return user ? user.uid : null;
    },
    async logout() {
      await auth.signOut();
    },
  }
};
