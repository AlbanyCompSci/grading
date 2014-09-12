var ids = [];
$('[id]').each(function() {
    id = $(this).attr('id')
    if (/-editor$/.test(id)) {
        ids.push(id)
    }
})

var editors = [];
for (var i=0; i<ids.length; i++) {
    var editor = ace.edit(ids[i])
    editor.setTheme('ace/theme/clouds_midnight')
    editor.getSession().setMode('ace/mode/java')
    editors.push(editor)
}
