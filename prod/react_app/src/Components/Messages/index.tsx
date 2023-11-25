import { FC, useEffect } from "react";
import { IMessage } from "../../shared/types";
import { Message } from "./components/Message";
import "./Messages.scss";

export const Messages: FC<{ messages: IMessage[] }> = ({ messages }) => {
  useEffect(() => {
    const container = document.getElementById("messagesContainer");

    if (!container) {
      return;
    }

    container.scrollTop = container.scrollHeight;
  }, [messages]);

  return (
    <div id="messagesContainer" className="messages-container">
      {messages.map((message) => (
        <Message message={message} />
      ))}
    </div>
  );
};
