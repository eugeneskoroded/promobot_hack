export interface IMessage {
  performer?: string;
  group?: string;
  theme?: string;
  description?: string;
  isUser: boolean;
}
