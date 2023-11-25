import { FC } from "react";
import "./SvgIcon.scss";

export const SvgIcon: FC<{ iconId: string; className?: string }> = ({
  iconId,
  className,
}) => (
  <svg className={`svg-icon ${className ?? ""}`}>
    <use xlinkHref={`/icons.svg#${iconId}`} />
  </svg>
);
