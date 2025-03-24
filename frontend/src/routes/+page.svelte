<script lang="ts">
    import { onMount } from "svelte";
    import io, { Socket } from "socket.io-client";

    type Message = {
        user: string;
        timestamp: string;
        message: string;
    };

    let socket: Socket;
    let user = $state("");
    let message = $state("");
    let messages = $state<Array<Message>>([]);

    function sendMessage(event: KeyboardEvent) {
        if (event.key === "Enter") {
            fetch(import.meta.env.VITE_API_URL + "/messages", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    user: user,
                    timestamp: new Date().toISOString(),
                    message: message,
                }),
            }).then(() => {
                console.log("sent message.");
                message = "";
            });
        }
    }

    function retrieveMessages() {
        fetch(import.meta.env.VITE_API_URL + "/messages").then((res) => {
            res.json().then((value) => (messages = value));
        });
    }

    onMount(() => {
        const interval = setInterval(() => {
            retrieveMessages();
        }, 500);

        socket = io(import.meta.env.VITE_API_URL);

        socket.on("connect", () => {
            console.log("Connected to the server!");
            socket.emit("message", "Hello from the Svelte client!");
        });

        socket.on("response", (data) => {
            console.log("Server response:", data);
        });

        return () => {
            socket.disconnect();
            clearInterval(interval);
        };
    });
</script>

<div class="container">
    <div>
        <label for="user">User</label>
        <input id="user" type="text" bind:value={user} />
    </div>

    <div>
        <label for="message">Message</label>
        <input
            id="message"
            type="text"
            bind:value={message}
            onkeydown={(e) => sendMessage(e)}
        />
    </div>

    <div>
        {#each messages as msg}
            <div>
                {msg.timestamp}
                from: {msg.user}
                message: {msg.message}
            </div>
        {/each}
    </div>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
</style>
