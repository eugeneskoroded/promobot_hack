import axios from "axios";
import { IMessage } from "../shared/types";

const axiosInstance = axios.create({
  baseURL: "http://81.94.159.128:8081",
});

export const sendMessage = async (
  message: string,
  withAiAssistant: boolean,
): Promise<IMessage> => {
  const { data } = await axiosInstance.post<IMessage>("/send_message", {
    message,
    withAiAssistant,
  });
  return data;
};
