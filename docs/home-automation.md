# Home automation

## Home Assistant

The Home Assistant configuration is maintained separately in the
[HomeAssistant repository](https://github.com/imnotdev25/HomeAssistant).
Keep this repository focused on the wider homelab topology and link to that
repository for Home Assistant configuration changes.

## RF fan control bridge

The fan's original RF remote was reverse-engineered with an RF receiver. The
captured RF control was then exposed through an ESPHome bridge, allowing Home
Assistant to operate the fan as part of automations and the user interface.

Document the following alongside the ESPHome configuration, without committing
the values here:

- RF receiver/transmitter model and GPIO wiring
- Captured protocol, code values, and pulse timing
- ESPHome device name, Wi-Fi secret reference, and Home Assistant entity IDs
- Safe fan states after a bridge reboot or loss of connectivity

## Remote access and identity

Cloudflared provides Home Assistant's public ingress through Cloudflare Tunnel.
Logto provides OIDC authentication for the lab's identity-aware services. The
operational model is:

1. Cloudflare receives the public request and forwards it through the tunnel.
2. Home Assistant remains off the directly exposed home-network edge.
3. Tailscale remains the preferred private administration route.
4. OIDC client configuration and tunnel credentials remain in secret stores.

Before changing any authentication or tunnel settings, record a recovery path
that still works if the identity provider, tunnel, or public DNS is unavailable.
