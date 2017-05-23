/**
 * Created by newmember on 17/05/2017.
 */

define([
	"dojo/_base/declare",
	"dojo/_base/lang",
	"dojo/dom-style",
	'dojo/request/xhr',
	"dojo/on",
	"dojo/cookie",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dojo/text!./templates/GreetingWidget.html"
], function (declare, lang, domStyle, xhr, on, cookie, _WidgetBase, _TemplatedMixin, template) {
	return declare("GreetingWidget", [_WidgetBase, _TemplatedMixin], {
		author: "Anonymous",
		avatarEdit: require.toUrl("../static/images/edit.png"),
		avatarDelete: require.toUrl("../static/images/delete.png"),
		templateString: template,
		baseClass: "greetingWidget",

		postCreate: function () {
			this.inherited(arguments);
			this._showAndHideEditContent(true);

			this.own(
					on(this.avatarEditNode, "click", lang.hitch(this, "_clickEdit")),
					on(this.avatarDeleteNode, "click", lang.hitch(this, "_clickDelete")),
					on(this.submitNode, "click", lang.hitch(this, "_clickSubmit"))
			);
		},

		_clickEdit: function () {
			this._showAndHideEditContent(false);
		},

		_clickSubmit: function () {
			var instance = this;
			var content = this.editContentNode.value;
			xhr.put(this.url, {
				data: JSON.stringify({message : content}),
				headers: {
					"X-CSRFToken": cookie("csrf_token")
				}
			}).then(function (data) {
				instance._showAndHideEditContent(true);
				alert("Update successed."+ data)
			}, function () {
				alert("Update failed.")
			});
		},

		_showAndHideEditContent: function (value) {
			if (value){
				domStyle.set(this.informationNode, "display", "block");
				domStyle.set(this.formEditNode, "display", "None");
			}else{
				domStyle.set(this.informationNode, "display", "None");
				domStyle.set(this.formEditNode, "display", "block");
			}
		},

		_clickDelete: function () {
			if (confirm("Are you sure to delete?")) {
				xhr.del(this.url, {
					headers: {
						"X-CSRFToken": cookie("csrf_token")
					}
				}).then(function () {
					alert("Delete successed.")
				}, function () {
					alert("Deleted failed.")
				});
			}
		},

		_setAvatarEditAttr: function (imagePath) {
			if (imagePath != "") {
				this._set("avatarEdit", imagePath);
				this.avatarEditNode.src = imagePath;
			}
		},

		_setAvatarDeleteAttr: function (imagePath) {
			if (imagePath != "") {
				this._set("avatarDelete", imagePath);
				this.avatarDeleteNode.src = imagePath;
			}
		},
	});
});
