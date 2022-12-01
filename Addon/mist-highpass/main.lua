SLASH_HIGHPASS1 = "/highpass"

function KethoEditBox_Show(text)
   if not KethoEditBox then
      local f = CreateFrame("Frame", "KethoEditBox", UIParent, "DialogBoxFrame")
      f:SetPoint("CENTER")
      f:SetSize(600, 500)

      f:SetBackdrop(
         {
            bgFile = "Interface\\DialogFrame\\UI-DialogBox-Background",
            edgeFile = "Interface\\PVPFrame\\UI-Character-PVP-Highlight", -- this one is neat
            edgeSize = 16,
            insets = { left = 8, right = 6, top = 8, bottom = 8 }
         }
      )
      f:SetBackdropBorderColor(0, .44, .87, 0.5) -- darkblue

      -- Movable
      f:SetMovable(true)
      f:SetClampedToScreen(true)
      f:SetScript(
         "OnMouseDown",
         function(self, button)
            if button == "LeftButton" then
               self:StartMoving()
            end
         end
      )
      f:SetScript("OnMouseUp", f.StopMovingOrSizing)

      -- ScrollFrame
      local sf = CreateFrame("ScrollFrame", "KethoEditBoxScrollFrame", KethoEditBox, "UIPanelScrollFrameTemplate")
      sf:SetPoint("LEFT", 16, 0)
      sf:SetPoint("RIGHT", -32, 0)
      sf:SetPoint("TOP", 0, -16)
      sf:SetPoint("BOTTOM", KethoEditBoxButton, "TOP", 0, 0)

      -- EditBox
      local eb = CreateFrame("EditBox", "KethoEditBoxEditBox", KethoEditBoxScrollFrame)
      eb:SetSize(sf:GetSize())
      eb:SetMultiLine(true)
      eb:SetAutoFocus(false) -- dont automatically focus
      eb:SetFontObject("ChatFontNormal")
      eb:SetScript(
         "OnEscapePressed",
         function()
            f:Hide()
         end
      )
      sf:SetScrollChild(eb)

      -- Resizable
      f:SetResizable(true)

      local rb = CreateFrame("Button", "KethoEditBoxResizeButton", KethoEditBox)
      rb:SetPoint("BOTTOMRIGHT", -6, 7)
      rb:SetSize(16, 16)

      rb:SetNormalTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Up")
      rb:SetHighlightTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Highlight")
      rb:SetPushedTexture("Interface\\ChatFrame\\UI-ChatIM-SizeGrabber-Down")

      rb:SetScript(
         "OnMouseDown",
         function(self, button)
            if button == "LeftButton" then
               f:StartSizing("BOTTOMRIGHT")
               self:GetHighlightTexture():Hide() -- more noticeable
            end
         end
      )
      rb:SetScript(
         "OnMouseUp",
         function(self, button)
            f:StopMovingOrSizing()
            self:GetHighlightTexture():Show()
            eb:SetWidth(sf:GetWidth())
         end
      )
      f:Show()
   end

   if text then
      KethoEditBoxEditBox:SetText(text)
   end
   KethoEditBox:Show()
end

function getReagentName(name, itemID)
   local quality_table =
   {
      [1] = "Bronze",
      [2] = "Silver",
      [3] = "Gold",
      [4] = "Diamond",
      [5] = "Mythic"
   };
   local quality = quality_table[C_TradeSkillUI.GetItemReagentQualityByItemInfo(itemID)]
   if quality then
      return quality .. " " .. name
   else
      return name
   end
end

function GenerateReagentReportHandler()
   -- generate output dictionary
   local output = {}
   for i = 1, GetInboxNumItems() do
      local _, _, sender, subject, _, _, _, hasItem = GetInboxHeaderInfo(i)
      if hasItem then
         for j = 1, ATTACHMENTS_MAX_RECEIVE do
            local name, itemID, texture, count, quality, canUse = GetInboxItem(i, j)
            
            
            if name then
               local outputName = getReagentName(name, itemID)
               if not output[sender] then
                  output[sender] = {}
               end
               local newTotal = (output[sender][outputName] or 0) + count
               output[sender][outputName] = newTotal
            end
         end
      else
         print("Message", subject, "from", sender, "has no attachments.")
      end
   end

   -- generate output text
   local outputText = ""
   for k, v in pairs(output) do
      outputText = outputText .. k .. "\n"
      for k2, v2 in pairs(v) do
         outputText = outputText .. "-" .. k2 .. "*" .. v2 .. "\n"
      end
   end
   KethoEditBox_Show(outputText)
end

function CallGenerateReagentReportSafely()
   local success, err = pcall(GenerateReagentReportHandler)
   if not success then
      print("Error:", err)
   end
end

SlashCmdList["HIGHPASS"] = CallGenerateReagentReportSafely
