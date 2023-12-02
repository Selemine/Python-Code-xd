export function errorMessage(err) {
  if (!err) {
    return;
  }
  const userNotFound = "auth/user-not-found";
  const authWrongPassword = "auth/wrong-password";
  const unknownError = "unknown";
	const emailIsUsed = "auth/email-already-in-use"
	const manyTries = "auth/too-many-requests"

  const errors = new Map([
    [userNotFound, "Такого пользователя не существует"],
    [authWrongPassword, "Неверный пароль или почта"],
		[emailIsUsed, "Почта уже используется"],
		[manyTries, "Слишком много попыток. Попробуйте зайти позже"],
    [unknownError, "Что-то пошло не так"],
  ]);

  if (err.code) {
    return errors.get(err.code) || errors.get(unknownError);
  }

  return errors.get(unknownError);
}
