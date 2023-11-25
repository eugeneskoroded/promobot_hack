import promobotLogo from "/logo-promobot.png";

export const Header = () => {
  return (
    <a
      href="https://promo-bot.ru/"
      target="_blank"
      style={{ width: "fit-content" }}
    >
      <img src={promobotLogo} alt="logo" width="145" height="45" />
    </a>
  );
};
