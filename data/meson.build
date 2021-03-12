desktop_file = i18n.merge_file(
  input: 'com.github.KrispyCamel4u.sysmontask.desktop.in',
  output: 'com.github.KrispyCamel4u.sysmontask.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'com.github.KrispyCamel4u.sysmontask.appdata.xml.in',
  output: 'com.github.KrispyCamel4u.sysmontask.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('icons/SysMonTask.png',
  install_dir: join_paths(get_option('datadir'), 'sysmontask/icons')
)

install_data('com.github.KrispyCamel4u.sysmontask.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif
