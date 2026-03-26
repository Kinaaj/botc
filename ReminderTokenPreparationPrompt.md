# Reminder Token Preparation Prompt

To prepare the reminder tokens for a specific set, please follow these instructions:

1.  **Set Specification:** The target set is `[SET_NAME]` (e.g., `05_Experimental`).
2.  **Role Translation:** Use `Encyklopedie - Role.csv` to translate the role names from English to Czech.
3.  **Keyword Mapping:** Use `reminder_keywords_mapping.csv` to map English keywords found in the `ReminderIconPNG` filenames to their Czech translations and the correct SVG template from `Templates/ReminderTokenTemplates/`.
4.  **Filename Construction:**
    *   If a keyword has a known translation (e.g., `Dead` -> `Mrtvy`), the new filename should be `[RoleCzechName][KeywordCzechName]ReminderTokenLaser.svg`.
    *   If a keyword translation is prefixed with `XXX` in the mapping file, use `XXX[RoleCzechName][KeywordEnglishName]ReminderTokenLaser.svg` and use the default `ReminderTokenLaser.svg` template.
5.  **Target Directory:** Place the generated SVG files into `Sets/[SET_NAME]/ReminderTokenLaser/`.
6.  **Edge Cases:** If a filename contains multiple keywords or numbers (e.g., `Dead0`), handle them by appending the suffix or merging the translations appropriately.

## Example:
For `LleechDead.png` in set `04_Experimental`:
- Role: `Lleech` -> `Pijavice` (from `Encyklopedie - Role.csv`)
- Keyword: `Dead` -> `Mrtvy` (from `reminder_keywords_mapping.csv`)
- Template: `MrtvyReminderTokenLaser.svg`
- Result: `Sets/04_Experimental/ReminderTokenLaser/PijaviceMrtvyReminderTokenLaser.svg`

For `AcrobatChosen.png`:
- Role: `Acrobat` -> `Akrobat`
- Keyword: `Chosen` -> `XXXChosen`
- Template: `ReminderTokenLaser.svg`
- Result: `Sets/04_Experimental/ReminderTokenLaser/XXXAkrobatChosenReminderTokenLaser.svg`
