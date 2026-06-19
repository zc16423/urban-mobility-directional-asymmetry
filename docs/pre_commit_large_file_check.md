# Pre-Commit Large File Check

## Purpose

Use these checks before any commit to avoid accidentally tracking large data files in ordinary Git. This repository is designed as a code/documentation repository with full data hosted externally.

## PowerShell Check

List files over 100 MB in the working tree:

```powershell
Get-ChildItem -Recurse -File -Force |
  Where-Object { $_.FullName -notmatch '\\.git\\' -and $_.Length -gt 100MB } |
  Sort-Object Length -Descending |
  Select-Object FullName,@{Name='SizeMB';Expression={[math]::Round($_.Length/1MB,1)}}
```

## Git Tracked File Check

After `git init` and before commit, list tracked or staged files over 100 MB:

```powershell
git ls-files -s | ForEach-Object { ($_ -split '\s+')[-1] } | Sort-Object -Unique | ForEach-Object {
  if (Test-Path -LiteralPath $_) {
    $item = Get-Item -LiteralPath $_
    if ($item.Length -gt 100MB) {
      [PSCustomObject]@{Path=$_; SizeMB=[math]::Round($item.Length/1MB,1)}
    }
  }
}
```

Check ignored state for important files:

```powershell
git check-ignore -v README.md .gitignore rename_map.md workflow.md docs/large_file_inventory.md docs/data_hosting_plan.md docs/github_upload_plan.md docs/reproducibility_notes.md
```

Expected result for the command above: no output for those key documentation files.

## Expected Result

- No ordinary-Git tracked file should exceed 100 MB.
- Large data directories should be ignored unless an explicit Git LFS policy is approved.
- Code, docs, manuscript source, and sample/example allowlisted files should remain trackable.

## What To Do If Large Files Are Listed

1. Do not commit.
2. Confirm whether the file belongs in the external data archive.
3. Update `.gitignore` or archive instructions if needed.
4. If Git LFS is intentionally chosen, copy and adapt `docs/gitattributes_lfs_draft.txt` to root `.gitattributes` only after approval.
5. Re-run the checks before committing.

## Latest Pre-Commit Scan Result

- Scan date: 2026-06-19.
- Git repository initialized: yes.
- Remote configured: no.
- Staged files: none.
- Dry-run command: `git -c safe.directory=I:/0git上传 add --dry-run .`.
- Proposed first-commit files: 57.
- Files over 100 MB proposed for Git: 0.
- Files over 500 MB proposed for Git: 0.

## Files Over 100 MB In Working Tree

| Relative path | Size | Extension |
| --- | --- | --- |
| figure_4/Fig4B/Fig4B_processed_data_all_R_ge_0.csv | 848.7 MB | .csv |
| figure_4/Fig4CD/fig4B_processed_data_all_R_ge_0.csv | 848.7 MB | .csv |
| figure_4/Fig4B/basic_data/Final_Regression_Dataset.csv | 762.1 MB | .csv |
| city_distance_matrices/Los Angeles.csv | 708.8 MB | .csv |
| figure_4/Fig4B/basic_data/distance_matrices/Los Angeles.csv | 708.8 MB | .csv |
| figure_4/Fig4B/basic_data/Link_Level_Realization_Ratio.csv | 691.5 MB | .csv |
| city_distance_matrices/New York.csv | 672.3 MB | .csv |
| figure_4/Fig4B/basic_data/distance_matrices/New York.csv | 672.3 MB | .csv |
| basic_data/real_year/Los Angeles.csv | 610.7 MB | .csv |
| figure_3/Fig3B/gravity/Los Angeles.csv | 610.7 MB | .csv |
| figure_4/Fig4B/basic_data/gravity/Los Angeles.csv | 610.7 MB | .csv |
| basic_data/real_year/New York.csv | 566.0 MB | .csv |
| figure_3/Fig3B/gravity/New York.csv | 566.0 MB | .csv |
| figure_4/Fig4B/basic_data/gravity/New York.csv | 566.0 MB | .csv |
| basic_data/choice_iom_year/New York.csv | 421.3 MB | .csv |
| basic_data/iom_year/New York.csv | 389.1 MB | .csv |
| basic_data/cumulative_intervening_opportunity_matrices/Los Angeles_opportunity_matrix.csv | 384.2 MB | .csv |
| basic_data/iom_year/Los Angeles.csv | 381.8 MB | .csv |
| basic_data/path_intervening_opportunity_matrices/Los Angeles_path_opportunity_matrix.csv | 380.3 MB | .csv |
| basic_data/cumulative_intervening_opportunity_matrices/New York_opportunity_matrix.csv | 361.3 MB | .csv |
| basic_data/path_intervening_opportunity_matrices/New York_path_opportunity_matrix.csv | 357.5 MB | .csv |
| basic_data/choice_iom_year/Los Angeles.csv | 318.9 MB | .csv |
| city_distance_matrices/Chicago.csv | 276.5 MB | .csv |
| figure_4/Fig4B/basic_data/distance_matrices/Chicago.csv | 276.5 MB | .csv |
| basic_data/real_year/Chicago.csv | 234.0 MB | .csv |
| figure_3/Fig3B/gravity/Chicago.csv | 234.0 MB | .csv |
| figure_4/Fig4B/basic_data/gravity/Chicago.csv | 234.0 MB | .csv |
| basic_data/iom_year/Chicago.csv | 213.5 MB | .csv |
| basic_data/choice_iom_year/Chicago.csv | 170.4 MB | .csv |
| basic_data/gravity_year/Los Angeles.csv | 158.6 MB | .csv |
| figure_1/Fig1A/real_year/Los Angeles.csv | 158.6 MB | .csv |
| figure_3/Fig3B/real/Los Angeles.csv | 158.6 MB | .csv |
| figure_4/Fig4B/basic_data/real/Los Angeles.csv | 158.6 MB | .csv |
| basic_data/gravity_year/New York.csv | 149.6 MB | .csv |
| figure_1/Fig1A/real_year/New York.csv | 149.6 MB | .csv |
| figure_3/Fig3B/real/New York.csv | 149.6 MB | .csv |
| figure_4/Fig4B/basic_data/real/New York.csv | 149.6 MB | .csv |
| basic_data/cumulative_intervening_opportunity_matrices/Chicago_opportunity_matrix.csv | 147.8 MB | .csv |
| basic_data/path_intervening_opportunity_matrices/Chicago_path_opportunity_matrix.csv | 145.4 MB | .csv |
| city_distance_matrices/Phoenix.csv | 108.6 MB | .csv |
| figure_4/Fig4B/basic_data/distance_matrices/Phoenix.csv | 108.6 MB | .csv |
| basic_data/iom_year/Phoenix.csv | 106.5 MB | .csv |

## Files Over 100 MB Proposed For Git

No files over 100 MB are proposed for the first commit.

## Decision

The working tree still contains large local research data, but the current `.gitignore` prevents those files from entering the dry-run first commit. The dry-run passes the large-file safety check.
