importScripts(
    "https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js"
);

importScripts(
    "https://www.gstatic.com/firebasejs/10.8.0/firebase-messaging-compat.js"
);

firebase.initializeApp({
    apiKey: "YOUR_API_KEY",
    authDomain: "test-project-49268.firebaseapp.com",
    projectId: "test-project-49268",
    storageBucket: "test-project-49268.firebasestorage.app",
    messagingSenderId: "309520688010",
    appId: "1:309520688010:web:fd2b94029d20ab86ac5e73"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(
    function(payload) {

        console.log(
            "[firebase-messaging-sw.js] Background Message",
            payload
        );

        self.registration.showNotification(
            payload.notification.title,
            {
                body: payload.notification.body
            }
        );
    }
);