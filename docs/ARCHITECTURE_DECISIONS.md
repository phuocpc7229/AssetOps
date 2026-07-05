# Architecture Decisions

## Future Asset Network Model

Status: Planned

Decision: Future asset network data should use the relationship `Asset -> NetworkInterface -> IPAddress`.

Reason: Real devices can have multiple network interfaces. Each interface has its own MAC address and can have one or more IP addresses. The current asset-level MAC/IP shape is too flat for accurate network inventory and monitoring.

Impact: This model refactor is required before implementing Monitoring, SNMP, traffic collection, or related network integrations. The model is not implemented yet.
