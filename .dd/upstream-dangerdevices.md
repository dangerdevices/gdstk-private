https://github.com/heitzmann/gdstk has updated the default branch! This pull request merges those changes to our [`dangerdevices`] branch.

If you're planning to release a new version, please follow:

## Update this pull request

1. Merge the latest `dangerdevices`[^1] branch into this pull request's branch.

2. Update `include/gdstk/gdstk.hpp` with the incremented version. As a friendly reminder, we're following [PEP 440] so the version should be:

   ```
   {gdstk-upstream-version}+dd{local-release-count}
   ```

3. Update `pyproject.toml` with the same incremented version from step 2.

[`dangerdevices`]: https://github.com/dangerdevices/gdstk-private
[PEP 440]: https://www.python.org/dev/peps/pep-0440/#local-version-identifiers

## After merging this pull request

4. Create a GitHub Release e.g.,

   ```
   $ gh release create --target dangerdevices --title v{gdstk-upstream-version}+dd{local-release-count} v{gdstk-upstream-version}+dd{local-release-count}
   ```

   Please make sure to write the release notes separating the public and private changes. See the [`v0.8.1+dd1` release] as an example.

5. Publish the new release!

   _Note_: If you used `gh release create`, this does not update your local repository with the tags. You can retrieve the tags via `git fetch --tags`.

6. Update the respective projects to use the newly published release.

_This pull request was automatically created via [`upstream.yml`], a GitHub Action._

[`v0.8.1+dd1` release]: https://github.com/dangerdevices/gdstk-private/releases/tag/v0.8.1%2Bdd1
[`upstream.yml`]: https://github.com/dangerdevices/gdstk-private/blob/dangerdevices/.github/workflows/upstream.yml

[^1]: This pull request is only pulling in the latest upstream references. So, to keep the custom build of `dangerdevices`, the branch must be merged back in here.
