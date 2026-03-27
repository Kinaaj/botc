# Role Token Preparation Prompt

To prepare the role tokens for a specific set, please follow these instructions:

1.  **Set Specification:** The target set is `[SET_NAME]` (e.g., `01_TroubleBrewing`).
2.  **Initial Role Identification:** List all PNG files in `Sets/[SET_NAME]/RoleIconPNG/`. Use the filenames (without extension) as English role names.
3.  **Verification & Validation:** Cross-reference the identified roles with `Encyklopedie - Role.csv`:
    *   **Completeness:** Filter the CSV by the `edition` or `Edice` column for the target set. Ensure every role listed in the CSV has a corresponding file in the `RoleIconPNG` folder.
    *   **Quantity Check:** For each role in the CSV, check the `Role Token` column. Ensure that the number of tokens (SVG files) generated matches this value.
    *   **Suffix Handling:** If a role requires multiple tokens (e.g., `Imp`), the PNG files might have suffixes like `Imp0`, `Imp1`, etc. Ensure all variations are processed.
4.  **Role Translation:** Use `Encyklopedie - Role.csv` to map the English role names to their Czech translations (`name_cz`).
5.  **Template Usage:** Use `Templates/RoleTokenLaserTemplate.svg` as the base for all role tokens.
6.  **File Generation:**
    *   **Filename:** For each role/variation, create a copy of the template named `[RoleCzechName][OptionalSuffix]RoleTokenLaser.svg`.
    *   **Text Replacement:** Inside the SVG, find the text element (labeled "Text" or containing "Byrokrat") and replace the content of the `<tspan>` with the Czech name of the role (omit suffixes in the visual text).
7.  **Target Directory:** Place all generated SVG files into `Sets/[SET_NAME]/RoleTokenLaser/`.

## Example Verification:
For set `01_TroubleBrewing`:
- CSV says `Imp` (id 21) has `Role Token` = 4.
- `RoleIconPNG` contains `Imp0.png`, `Imp1.png`, `Imp2.png`, `Imp3.png`.
- Result: 4 SVG files generated (`Čert0RoleTokenLaser.svg` to `Čert3...`), all displaying "Čert".

For `Chef`:
- CSV says `Chef` (id 1) has `Role Token` = 1.
- `RoleIconPNG` contains `Chef.png`.
- Result: 1 SVG file `KuchařRoleTokenLaser.svg` displaying "Kuchař".
