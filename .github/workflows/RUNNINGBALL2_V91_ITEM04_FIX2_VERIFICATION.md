# RUNNINGBALL2 — Item 04 — V91 FIX2 verification
Date: 2026-10-27

## Observed failed build
- V89 FIX1 GitHub Actions run: https://github.com/Sentongoharuna/Duwm/actions/runs/40498552077
- APK compiled, signed and installed on emulator; inherited early navigation tests passed.
- Failed at `AssertionError: ITEM02 register search field missing` in the inherited emulator smoke test.

## Exact cause
- The actual `RunningballV25FlightRegisterActivity.java` creates a native `EditText` with `query.setHint("Search callsign, ICAO24, reported origin")`.
- The inherited emulator test calls `find('Search callsign, ICAO24, reported origin')`, which searches for ordinary accessible text. A hint may not be presented as an ordinary text node in Android's UI hierarchy.
- The previous V3 emulator gate entered the real register successfully and returned PASS. That evidence does not prove the later field text search is valid.

## Single repair
- Changed only the Item 02 emulator smoke-test selector: require `RunningballV25FlightRegisterActivity` foreground, identify an enabled `android.widget.EditText` node from Android UI hierarchy by its class and screen bounds, tap it, type valid test ICAO24 `0BAD00` (lookup only; no fake aircraft record), tap existing `OPEN ICAO24 OPEN SKY DETAILS` and require `AirFlightDetailsActivity` with correct OpenSky labels. The screen does not need the aircraft ID to be present; the activity must report missing data honestly.
- Added a fail-closed source / smoke-contract gate that checks the actual source field, the new native EditText selector, and preservation of real navigation.
- Original globe and wallpapers, Items 01–04, network sources and user-interface app source unchanged.
- Unique workflow name: `RUNNINGBALL2_V91_ITEM04_FIX2.yml`; versionCode 91; signed APK intended artifact `RUNNINGBALL2-ITEM04-V91-FIX2-SEARCH-REPAIR.apk`.

## Checks completed locally
- YAML parses successfully; all 76 workflow steps preserved (75 inherited plus one gate).
- Bash syntax checks pass on all shell steps.
- Emulator test-generation Python parses; no exact-hint text lookup remains in the generated test snippet.
- Native EditText inspection logic tested with a representative XML accessibility node where the hint is present only as a hint and `node.text` is empty; text-based search cannot find it, native-control search does.
- Register source archive inspected; actual `query=new EditText(this)` and its hint exist.
- Filename consistency and versionCode 91 checked.

## NOT verified
- V91 GitHub Android build, screenshot, or device behavior. A successful prior V89 FIX1 APK does not establish V91 emulator success.
- The fix targets a specific bad test selector; any newly revealed error will need its own evidence-driven repair.

## Release decision
- A new workflow is prepared for GitHub. Item 05 was NOT started. Do not claim V91 is green until the Actions job completes and the actual Item 02 native navigation gate passes.
