# Parameters from earlier ARR workflows

Movie adds use `arr_target="radarr"` and TMDb/IMDb IDs or a title query. Series adds use `arr_target="sonarr"` and TVDb/IMDb IDs or a title query. Carry profile, root, monitoring and search preferences into `options`.

The earlier Sonarr workflow used `${SONARR_URL}`; use that host only when selected by the user or established environment, not as a universal default. [Connection and defaults](connection-defaults.md) defines host resolution and defaults.
