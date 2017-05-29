/**
 * Created by newmember on 17/05/2017.
 */

define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/cookie",
	"dojo/dom-style",
	"dojo/on",
	'dojo/request/xhr',
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dojo/text!./templates/GreetingWidget.html"
], function (declare, lang, cookie, domStyle, on, xhr, _WidgetBase, _TemplatedMixin, template) {
	return declare("GreetingWidget", [_WidgetBase, _TemplatedMixin], {
		author: "Anonymous",
		templateString: template,
		baseClass: "greetingWidget",
		_isEdit: false,

		postCreate: function () {
			this.inherited(arguments);
			this._toggleEdit();
			this.own(
					on(this.editNode, "click", lang.hitch(this, function () {
						this._toggleEdit();
					})),
					on(this.deleteNode, "click", lang.hitch(this, "_clickDelete")),
					on(this.submitNode, "click", lang.hitch(this, "_clickSubmit"))
			);
		},

		_clickSubmit: function () {
			var content = this.editContentNode.value;
			var instance = this;
			xhr.put(this.url, {
				data: JSON.stringify({message : content}),
				headers: {
					"X-CSRFToken": cookie("csrf_token")
				}
			}).then(function (data) {
				instance._toggleEdit(true);
				alert("Update successed."+ data)
			}, function (data) {
				alert("Update failed."+ data)
			});
		},

		_toggleEdit: function (){
			if (this._isEdit){
				domStyle.set(this.informationNode, "display", "None");
				domStyle.set(this.formEditNode, "display", "block");
				this._isEdit = false;
			}else{
				domStyle.set(this.informationNode, "display", "block");
				domStyle.set(this.formEditNode, "display", "None");
				this._isEdit = true;
			}
		},

		_clickDelete: function () {
			if (confirm("Are you sure to delete?")) {
				xhr.del(this.url, {
					headers: {
						"X-CSRFToken": cookie("csrf_token")
					}
				}).then(function (data) {
					alert("Delete successed."+data)
				}, function (data) {
					alert("Deleted failed."+data)
				});
			}
		},
	});
});
