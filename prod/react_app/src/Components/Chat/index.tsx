import "./Chat.scss";
import {
  Checkbox,
  CircularProgress,
  FormControlLabel,
  IconButton,
  InputAdornment,
  TextField,
} from "@mui/material";
import { ChangeEvent, useState } from "react";
import { IMessage } from "../../shared/types";
import { Messages } from "../Messages";
import { sendMessage } from "../../api";
import { SvgIconIds } from "../../shared/components/SvgIcon/SvgIcon.types.ts";
import { SvgIcon } from "../../shared/components/SvgIcon";

export const Chat = () => {
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [currentMessage, setCurrentMessage] = useState<string>("");
  const [withAiAssistant, setWithAiAssistant] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);

  const handleMessageInput = (event: ChangeEvent<HTMLInputElement>) => {
    setCurrentMessage(event.target.value);
  };
  const handleSendClick = async () => {
    if (!currentMessage.length) {
      return;
    }

    try {
      setLoading(true);

      const botMessage = await sendMessage(currentMessage, withAiAssistant);

      setMessages((prev) => [
        ...prev,
        { isUser: true, description: currentMessage },
        botMessage,
      ]);

      setCurrentMessage("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-content">
      <Messages messages={messages} />
      <div className="controls">
        <FormControlLabel
          label="Использовать AI"
          title="Использовать AI"
          labelPlacement="start"
          id="checkbox"
          disabled={loading}
          control={
            <Checkbox
              color="primary"
              checked={withAiAssistant}
              onChange={({ target: { checked: targetChecked } }) =>
                setWithAiAssistant(targetChecked)
              }
            />
          }
        />
        <TextField
          multiline
          placeholder="Опишите вашу проблему..."
          minRows={2}
          maxRows={5}
          disabled={loading}
          onInput={handleMessageInput}
          value={currentMessage}
          InputProps={{
            className: "message-text",
            endAdornment: (
              <InputAdornment position="end">
                {loading ? (
                  <CircularProgress className="loader" />
                ) : (
                  <IconButton
                    className="send-button"
                    onClick={handleSendClick}
                    hidden={!currentMessage.length}
                  >
                    <SvgIcon
                      iconId={SvgIconIds.SEND_MESSAGE}
                      className="send-icon"
                    />
                  </IconButton>
                )}
              </InputAdornment>
            ),
          }}
        />
      </div>
    </div>
  );
};
