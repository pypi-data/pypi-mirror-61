# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]


## [0.2.1] - 2020-02-10
### Changed
- **countries**
    - Use **utils.UpAndDownIsActiveMixin**
- **companies**
    - Use **utils.UpAndDownIsActiveMixin**
    
### Fixed
- UpIsActiveTestCase was simplified
- Redefine global package testing


## [0.2.0] - 2020-02-04
### Added
- **utils**
    - **UpIsActiveMixin**, a mixin that contain an *is_active* field and change its value to True in an upward cascade (a class with that mixin will have its parents *is_active* field modified).
    - **DownIsActiveMixin**, a mixin that contain an *is_active* field and change its value to False in an downward cascade (a class with that mixin will have its children *is_active* field modified).
    - **UpAndDownIsActiveMixin**, a mixin that contain Up and Down IsActive Mixins.
    - Added an **ActiveQuerySet** class with two methods:
        - 'active' returns only the active objects
        - 'inactive' returns only the inactive objects
- **companies**, an application with models specific to a company structure
    - An abstract model:
        - **AbstractCompanyModel**, a model to host all common fields between the 'companies' objects
            - **linked_services**, a method that returns a Queryset with the services linked to any company Object (*Note:* Needs to be implemented if you use this abstract model)
    - 3 Levels of models:
        - **Service**, a branch of a subsidiary (ex: Accounting)
        - **Subsidiary**, a part of a company (ex: ACME France)
        - **Company**, a company (ex: ACME)
        - **CompanyGroup**, a group of company (ex: ACME Holding)
    - A simple administration interface for all the models above, generated automatically
    - A custom command to generate fake company data, *generate_fake_companies_data*
    
### Changed
- **countries**
    - Use **utils.ActiveQuerySet** for the base manager
- **utils**
    - Moved *models* to *models_mixins*, as it is a better description of the content of this file
    
### Removed
- **utils**
    - **ModelMixinTestCase**, as it was unnecessary and also a headache to use alongside migrations


## [0.1.1] - 2020-01-22
### Fixed
- Added the countries/migrations_files directory to the package setup (migrations wouldn't work)


## [0.1.0] - 2020-01-14
### Added
- **countries**, an application with models specific to a location:
    - An abstract model:
        - **LocBaseAbstractModel**, a model to host all common fields between the 'locations' objects
            - **linked_countries**, a method that returns a Queryset with the countries linked to any Loc Object (*Note:* Needs to be implemented if you use this abstract model)
    - 3 Levels of models:
        - **Country**, a model to host a country as defined by the **ISO 3166** norm.
        - **SubRegion**, a group of multiple Countries
        - **Region**, a group of multiple SubRegions
    - A simple administration interface for all the models above
    - A custom data migrations to add all the countries and default SubRegions and Regions.
- **utils**, a subpackage for simple tools we use on a daily basis:
    - An admin file with useful mixins:
        - **NoCreateModelAdminMixin**, a mixin to remove the create ability of an admin object
        - **NoChangeModelAdminMixin**, a mixin to remove the change ability of an admin object
        - **NoDeleteModelAdminMixin**, a mixin to remove the delete ability of an admin object
        - **ReadOnlyModelAdmin**, a model to remove all actions of the admin, making it read-only
        - **NoCreateInlineModelAdminMixin**, a mixin to remove the create ability of an inline object
        - **NoChangeInlineModelAdminMixin**, a mixin to remove the change ability of an admin object
    - A models file with useful mixins:
        - **NotModifiableFieldsModelMixin**, a mixin that allows you to create fields that can't be modified after the instance is saved in datatabase
        - **AbrModelMixin**, a mixin to add an optional abbreviation to a model
            - *get_name_or_abbreviation*, a method that returns the abbreviation if specified, a name if specified, or None
    - A testcase file with useful testcases classes:
        - **ModelMixinTestCase**, a testcase that allows you to do mixin testing (creating the model in database for the tests)
        - **CountSaveModelMixin**, a mixin that will count the number of time .save() is called for unit testing purposes


## [0.0.dev4] - 2020-01-02
- Simple badges for the supported versions of Django/Python

### Changed
- The badges links are simplified


## [0.0.dev3] - 2019-12-26
### Added
- A MANIFEST.in file to keep external files in the package ifneeded

### Changed
- Updated README with working instructions on how to upload a package and fixed code snippets

### Fixed
- Fixed the supported versions of python and Django:
    - Supported Django versions are 2.2 and 3.0
    - Supported Python version are >=3.5 for Django 2.2 and >=3.6 for Django 3.0
- Fixed the CHANGELOG links


## [0.0.dev2] - 2019-12-23
### Added
- CHANGELOG.md file based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
- Updated README with upload instructions


## [0.0.dev1] - 2019-12-20
### Added
- The package skeleton


[Unreleased]: https://bitbucket.org/pixelforest/pixelforest_drf/branches/compare/HEAD%0D0.2.1
[0.2.1]: https://bitbucket.org/pixelforest/pixelforest_drf/branches/compare/0.2.1%0D0.2.0
[0.2.0]: https://bitbucket.org/pixelforest/pixelforest_drf/branches/compare/0.2.0%0D0.1.1
[0.1.1]: https://bitbucket.org/pixelforest/pixelforest_drf/branches/compare/0.1.1%0D0.1.0
[0.1.0]: https://bitbucket.org/pixelforest/pixelforest_drf/branches/compare/0.1.0%0D0.0.dev4
[0.0.dev4]: https://bitbucket.org/pixelforest/pixelforest_drf/branches/compare/0.0.dev4%0D0.0.dev3
[0.0.dev3]: https://bitbucket.org/pixelforest/pixelforest_drf/branches/compare/0.0.dev3%0D0.0.dev2
[0.0.dev2]: https://bitbucket.org/pixelforest/pixelforest_drf/branches/compare/0.0.dev2%0D0.0.dev1
[0.0.dev1]: https://bitbucket.org/pixelforest/pixelforest_drf/src/0.0.dev1/