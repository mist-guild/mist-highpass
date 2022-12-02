SLASH_HIGHPASS1 = "/highpass"

local function getBOEName(itemRarity)
   local quality_table =
   {
      [0] = "Poor",
      [1] = "Common",
      [2] = "Uncommon",
      [3] = "Rare",
      [4] = "Epic"
   };
   local quality = quality_table[itemRarity];
   return "BOE" .. "*" .. quality;
end

local function getReagentName(name, itemID)
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
      return name .. "*" .. quality
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
            -- gather item info
            local name, itemID, texture, count, quality, canUse = GetInboxItem(i, j)
            if itemID == nil then
               break
            end
            _, _, itemRarity, _, _, itemType, itemSubType, _, _, _, _ = GetItemInfo(itemID)

            -- if found, add to output string
            if name then
               -- get name of item and rarity/quality
               local outputName = ""
               if itemType == "Armor" or itemType == "Weapon" then
                  outputName = getBOEName(itemRarity)
               else
                  outputName = getReagentName(name, itemID)
               end

               -- add to hashmap
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

   -- render output text
   highpass:KethoEditBox_Show(outputText)
end

function CallGenerateReagentReportSafely()
   local success, err = pcall(GenerateReagentReportHandler)
   if not success then
      print("Error:", err)
   end
end

SlashCmdList["HIGHPASS"] = CallGenerateReagentReportSafely
