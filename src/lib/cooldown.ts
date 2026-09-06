import { useState, useEffect } from "react";
import { User } from "./store";

const COOLDOWN_KEY = "ai_request_cooldown_timestamp";
const COOLDOWN_DURATION = 0; // Disabled

export function getAICooldownTimeRemaining(user: User | null): number {
  return 0;
}

export function triggerAICooldown(user: User | null): void {
  // Disabled
}

export function useAICooldown(user: User | null) {
  return {
    cooldownRemaining: 0,
    startCooldown: () => {}
  };
}
