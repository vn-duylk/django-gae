/**
 * Created by newmember on 17/05/2017.
 */

define([
	"dojo/_base/declare",
	"dojo/_base/fx",
	"dojo/_base/lang",
	"dojo/dom-style",
	"dojo/mouse",
	"dojo/on",
	"dojo/request",
	"dijit/_WidgetBase",
	"dijit/_TemplatedMixin",
	"dojo/text!./templates/GreetingWidget.html"
], function (declare, baseFx, lang, domStyle, mouse, on, request, _WidgetBase, _TemplatedMixin, template) {
	return declare("GreetingWidget", [_WidgetBase, _TemplatedMixin], {
		author: "Anonymous",
		content: "",
		guestbookId: "",
		date: "",
		dateUpdate: "",
		updatedBy: "",
		url: "",
		avatarEdit: require.toUrl("../static/images/edit.png"),
		avatarDelete: require.toUrl("../static/images/delete.png"),
		templateString: template,
		baseClass: "greetingWidget",
		mouseAnim: null,
		baseBackgroundColor: "#fff",
		mouseBackgroundColor: "#def",

		postCreate: function () {

			var domNode = this.domNode;

			this.inherited(arguments);

			domStyle.set(domNode, "backgroundColor", this.baseBackgroundColor);
			this.own(
					on(domNode, mouse.enter, lang.hitch(this, "_changeBackground", this.mouseBackgroundColor)),
					on(domNode, mouse.leave, lang.hitch(this, "_changeBackground", this.baseBackgroundColor)),
					on(this.avatarEditNode, "click", lang.hitch(this, "_clickEdit")),
					on(this.avatarDeleteNode, "click", lang.hitch(this, "_clickDelete"))
			);
		},

		_clickEdit: function(){
			if (confirm("Are you sure?")){
				console.log("yes");
			}

		},

		_clickDelete: function(){
			if (confirm("Are you sure?")){
				console.log("yes")
			}

		},

		_changeBackground: function (newColor) {
			if (this.mouseAnim) {
				this.mouseAnim.stop();
			}

			this.mouseAnim = baseFx.animateProperty({
				node: this.domNode,
				properties: {
					backgroundColor: newColor
				},
				onEnd: lang.hitch(this, function () {
					this.mouseAnim = null;
				})
			}).play();
		},

		_setAvatarEditAttr: function (imagePath) {
			if (imagePath != "") {
				this._set("avatarEdit", imagePath);
				this.avatarEditNode.src = imagePath;
			}
		},

		_setAvatarDeleteAttr: function (imagePath) {
			if (imagePath != ""){
				this._set("avatarDelete", imagePath);
				this.avatarDeleteNode.src = imagePath;
			}
		},
	});
});
