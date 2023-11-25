import { FC } from "react";
import { IMessage } from "../../../../shared/types";
import "./Message.scss";
import { SvgIcon } from "../../../../shared/components/SvgIcon";
import { SvgIconIds } from "../../../../shared/components/SvgIcon/SvgIcon.types.ts";

export const Message: FC<{ message: IMessage }> = ({ message }) => {
  if (message.isUser) {
    return (
      <div className="user-message">
        <div className="message-container user">
          <span className="message">{message.description}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bot-message">
      <SvgIcon className="portrait-icon" iconId={SvgIconIds.AI_PICTURE} />
      <div className="message-with-sender">
        <div className="message-container bot">
          <div className="promobot-message">
            <span className="message" hidden={!message.performer}>
              <span className="topic-text">Исполнитель:</span>{" "}
              {message.performer}
            </span>
            <span className="message" hidden={!message.group}>
              <span className="topic-text">Группа:</span> {message.group}
            </span>
            <span className="message" hidden={!message.theme}>
              <span className="topic-text">Тема:</span> {message.theme}
            </span>
            <span className="message" hidden={!message.description}>
              <span className="topic-text">Описание:</span>{" "}
              {message.description}
            </span>
          </div>
        </div>
        <span className="topic-text">Promobot AI</span>
      </div>
    </div>
  );
};
