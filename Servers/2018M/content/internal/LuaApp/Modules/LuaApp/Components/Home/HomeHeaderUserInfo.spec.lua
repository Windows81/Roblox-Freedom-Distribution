return function()
	local HomeHeaderUserInfo = require(script.Parent.HomeHeaderUserInfo)

	local Modules = game:GetService("CoreGui").RobloxGui.Modules

	local Roact = require(Modules.Common.Roact)
	local UserModel = require(Modules.LuaApp.Models.User)
	local FormFactor = require(Modules.LuaApp.Enum.FormFactor)

	local function MockHomeHeaderUserInfo(formFactor, membershipType)
		local localUserModel = UserModel.mock()
		localUserModel.membership = membershipType

		return Roact.createElement(HomeHeaderUserInfo, {
			localUserModel = localUserModel,
			formFactor = formFactor,
			sidePadding = 12,
			sectionPadding = 12,
		})
	end

	it("should create and destroy without errors", function()
		local element = MockHomeHeaderUserInfo(FormFactor.PHONE, Enum.MembershipType.None)

		local instance = Roact.mount(element)
		Roact.unmount(instance)
	end)

	describe("it should adapt to different formfactors", function()
		it("should render PHONE formfactor properly", function()
			local element = MockHomeHeaderUserInfo(FormFactor.PHONE, Enum.MembershipType.None)
			local container = Instance.new("Folder")
			Roact.mount(element, container, "Test")
			expect(container.Test:FindFirstChild("UserAvatar", true)).to.never.be.ok()
		end)

		it("should render TABLET formfactor properly", function()
			local element = MockHomeHeaderUserInfo(FormFactor.TABLET, Enum.MembershipType.None)
			local container = Instance.new("Folder")
			Roact.mount(element, container, "Test")
			expect(container.Test:FindFirstChild("UserAvatar", true)).to.be.ok()
		end)

		it("should render with an UNKNOWN formfactor without issues", function()
			local element = MockHomeHeaderUserInfo(FormFactor.UNKNOWN, Enum.MembershipType.None)
			local instance = Roact.mount(element)
			Roact.unmount(instance)
		end)
	end)

	describe("it should properly display user membership information", function()
		describe("should hide membership info if user is not a paid member", function()
			it("PHONE", function()
				local element = MockHomeHeaderUserInfo(FormFactor.PHONE, Enum.MembershipType.None)
				local container = Instance.new("Folder")
				Roact.mount(element, container, "Test")
				expect(container.Test:FindFirstChild("BuildersClub", true)).to.never.be.ok()
			end)

			it("TABLET", function()
				local element = MockHomeHeaderUserInfo(FormFactor.TABLET, Enum.MembershipType.None)
				local container = Instance.new("Folder")
				Roact.mount(element, container, "Test")
				expect(container.Test:FindFirstChild("BuildersClub", true)).to.never.be.ok()
			end)
		end)

		describe("should display membership info if user is a paid member", function()
			it("PHONE", function()
				local element = MockHomeHeaderUserInfo(FormFactor.PHONE, Enum.MembershipType.BuildersClub)
				local container = Instance.new("Folder")
				Roact.mount(element, container, "Test")
				expect(container.Test:FindFirstChild("BuildersClub", true)).to.be.ok()
			end)

			it("TABLET", function()
				local element = MockHomeHeaderUserInfo(FormFactor.TABLET, Enum.MembershipType.BuildersClub)
				local container = Instance.new("Folder")
				Roact.mount(element, container, "Test")
				expect(container.Test:FindFirstChild("BuildersClub", true)).to.be.ok()
			end)
		end)
	end)

end