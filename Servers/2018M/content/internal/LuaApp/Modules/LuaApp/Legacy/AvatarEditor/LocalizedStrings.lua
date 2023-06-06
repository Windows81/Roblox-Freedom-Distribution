local LocalizationService = game:GetService("LocalizationService")
local HttpService = game:GetService("HttpService")
local CoreGui = game:GetService('CoreGui')

local Modules = CoreGui:FindFirstChild("RobloxGui").Modules
local Flags = require(Modules.LuaApp.Legacy.AvatarEditor.Flags)
local LoadAvatarEditorTranslations = Flags:GetFlag("LoadAvatarEditorTranslations")

local this = {}

local function createLocalizationTable(contents)
	local localTable = Instance.new("LocalizationTable")
	localTable.SourceLocaleId = "en-us"
	localTable:SetContents(HttpService:JSONEncode(contents))
	return localTable
end

local AvatarEditorStringsTable = createLocalizationTable({
	{
		key = "FullViewWord";
		values =
		{
			["en-us"] = "Full View";
			["es"] = "Vista completa";
			["de"] = "Vollansicht";
			["fr"] = "Affichage complet";
			["pt-br"] = "Visão completa";
			["ko"] = "전체 보기";
			["zh-tw"] = "大螢幕";
			["zh-cn"] = "全视图";
		}
	},
	{
		key = "ReturnToEditWord";
		values =
		{
			["en-us"] = "Return to edit";
			["es"] = "Volver a edición";
			["de"] = "Zurück zum Bearbeiten";
			["fr"] = "Revenir à l'édition";
			["pt-br"] = "Voltar para editar";
			["ko"] = "편집으로 돌아가기";
			["zh-tw"] = "返回編輯";
			["zh-cn"] = "返回编辑";
		}
	},
	{
		key = "SwitchToR6Word";
		values =
		{
			["en-us"] = "Switch to R6";
			["es"] = "Cambiar a R6";
			["de"] = "Zu R6 wechseln";
			["fr"] = "Passer au modèle R6";
			["pt-br"] = "Trocar para R6";
			["ko"] = "R6로 전환";
			["zh-tw"] = "切換至 R6";
			["zh-cn"] = "转换至 R6";
		}
	},
	{
		key = "SwitchToR15Word";
		values =
		{
			["en-us"] = "Switch to R15";
			["es"] = "Cambiar a R15";
			["de"] = "Zu R15 wechseln";
			["fr"] = "Passer au modèle R15";
			["pt-br"] = "Trocar para R15";
			["ko"] = "R15로 전환";
			["zh-tw"] = "切換至 R15";
			["zh-cn"] = "转换至 R6";
		}
	},
	{
		key = "RecentCategoryTitle";
		values =
		{
			["en-us"] = "Recent";
			["es"] = "Recientes";
			["de"] = "Vor Kurzem verwendet";
			["fr"] = "Récents";
			["pt-br"] = "Recentes";
			["ko"] = "최근";
			["zh-tw"] = "近期使用";
			["zh-cn"] = "最近使用";
		}
	},
	{
		key = "ClothingCategoryTitle";
		values =
		{
			["en-us"] = "Clothing";
			["es"] = "Ropa";
			["de"] = "Kleidung";
			["fr"] = "Vêtements";
			["pt-br"] = "Roupas";
			["ko"] = "복장";
			["zh-tw"] = "衣物";
			["zh-cn"] = "服装";
		}
	},
	{
		key = "BodyCategoryTitle";
		values =
		{
			["en-us"] = "Body";
			["es"] = "Cuerpo";
			["de"] = "Körper";
			["fr"] = "Corps";
			["pt-br"] = "Corpo";
			["ko"] = "신체";
			["zh-tw"] = "身體";
			["zh-cn"] = "身体";
		}
	},
	{
		key = "AnimationCategoryTitle";
		values =
		{
			["en-us"] = "Animation";
			["es"] = "Animación";
			["de"] = "Animation";
			["fr"] = "Animation";
			["pt-br"] = "Animação";
			["ko"] = "애니메이션";
			["zh-tw"] = "動畫";
			["zh-cn"] = "动画";
		}
	},
	{
		key = "AnimationCategoryLandscapeTitle";
		values =
		{
			["en-us"] = "Animations";
			["es"] = "Animaciones";
			["de"] = "Animationen";
			["fr"] = "Animations";
			["pt-br"] = "Animações";
			["ko"] = "애니메이션";
			["zh-tw"] = "動畫";
			["zh-cn"] = "动画";
		}
	},
	{
		key = "OutfitsCategoryTitle";
		values =
		{
			["en-us"] = "Outfits";
			["es"] = "Conjuntos";
			["de"] = "Outfits";
			["fr"] = "Tenues";
			["pt-br"] = "Trajes";
			["ko"] = "옷차림";
			["zh-tw"] = "行頭";
			["zh-cn"] = "装扮";
		}
	},
	{
		key = "RecentAllTitle";
		values =
		{
			["en-us"] = "Recent All";
			["es"] = "Todos los recientes";
			["de"] = "Vor Kurzem verwendet: alles";
			["fr"] = "Récents (tous)";
			["pt-br"] = "Todos os recentes";
			["ko"] = "최근 전체";
			["zh-tw"] = "近期全部";
			["zh-cn"] = "最近全部";
		}
	},
	{
		key = "RecentAllLandscapeTitle";
		values =
		{
			["en-us"] = "All";
			["es"] = "Todos";
			["de"] = "Alle";
			["fr"] = "Tous";
			["pt-br"] = "Todos";
			["ko"] = "전체";
			["zh-tw"] = "全部";
			["zh-cn"] = "全部";
		}
	},
	{
		key = "RecentClothingTitle";
		values =
		{
			["en-us"] = "Recent Clothing";
			["es"] = "Ropa reciente";
			["de"] = "Vor Kurzem verwendet: Kleidung";
			["fr"] = "Vêtements récents";
			["pt-br"] = "Roupas recentes";
			["ko"] = "최근 복장";
			["zh-tw"] = "近期使用的衣物";
			["zh-cn"] = "最近使用的服装";
		}
	},
	{
		key = "RecentClothingLandscapeTitle";
		values =
		{
			["en-us"] = "Clothing";
			["es"] = "Ropa";
			["de"] = "Kleidung";
			["fr"] = "Vêtements";
			["pt-br"] = "Roupas";
			["ko"] = "복장";
			["zh-tw"] = "衣物";
			["zh-cn"] = "服装";
		}
	},
	{
		key = "RecentBodyTitle";
		values =
		{
			["en-us"] = "Recent Body";
			["es"] = "Cuerpos recientes";
			["de"] = "Vor Kurzem verwendet: Körper";
			["fr"] = "Corps récents";
			["pt-br"] = "Corpos recentes";
			["ko"] = "최근 신체";
			["zh-tw"] = "近期身體";
			["zh-cn"] = "最近使用的身体类型";
		}
	},
	{
		key = "RecentBodyLandscapeTitle";
		values =
		{
			["en-us"] = "Body";
			["es"] = "Cuerpo";
			["de"] = "Körper";
			["fr"] = "Corps";
			["pt-br"] = "Corpo";
			["ko"] = "신체";
			["zh-tw"] = "身體";
			["zh-cn"] = "身体类型";
		}
	},
	{
		key = "RecentAnimationsTitle";
		values =
		{
			["en-us"] = "Recent Animations";
			["es"] = "Animaciones recientes";
			["de"] = "Vor Kurzem verwendet: Animationen";
			["fr"] = "Animations récentes";
			["pt-br"] = "Animações recentes";
			["ko"] = "최근 애니메이션";
			["zh-tw"] = "近期使用的動畫";
			["zh-cn"] = "最近使用的动画";
		}
	},
	{
		key = "RecentAnimationsLandscapeTitle";
		values =
		{
			["en-us"] = "Animations";
			["es"] = "Animaciones";
			["de"] = "Animationen";
			["fr"] = "Animations";
			["pt-br"] = "Animações";
			["ko"] = "애니메이션";
			["zh-tw"] = "動畫";
			["zh-cn"] = "动画";
		}
	},
	{
		key = "RecentOutfitsTitle";
		values =
		{
			["en-us"] = "Recent Outfits";
			["es"] = "Vestimentas recientes";
			["de"] = "Vor Kurzem verwendet: Outfits";
			["fr"] = "Tenues récentes";
			["pt-br"] = "Trajes recentes";
			["ko"] = "최근 옷차림";
			["zh-tw"] = "近期使用的行頭";
			["zh-cn"] = "最近使用的装扮";
		}
	},
	{
		key = "RecentOutfitsLandscapeTitle";
		values =
		{
			["en-us"] = "Outfits";
			["es"] = "Conjuntos";
			["de"] = "Outfits";
			["fr"] = "Tenues";
			["pt-br"] = "Trajes";
			["ko"] = "옷차림";
			["zh-tw"] = "行頭";
			["zh-cn"] = "装扮";
		}
	},
	{
		key = "OutfitsTabTitle";
		values =
		{
			["en-us"] = "Outfits";
			["es"] = "Conjuntos";
			["de"] = "Outfits";
			["fr"] = "Tenues";
			["pt-br"] = "Trajes";
			["ko"] = "옷차림";
			["zh-tw"] = "行頭";
			["zh-cn"] = "装扮";
		}
	},
	{
		key = "OutfitsTabLandscapeTitle";
		values =
		{
			["en-us"] = "All";
			["es"] = "Todos";
			["de"] = "Alle";
			["fr"] = "Tous";
			["pt-br"] = "Todos";
			["ko"] = "전체";
			["zh-tw"] = "全部";
			["zh-cn"] = "全部";
		}
	},
	{
		key = "HatsTitle";
		values =
		{
			["en-us"] = "Hats";
			["es"] = "Sombreros";
			["de"] = "Hüte";
			["fr"] = "Chapeaux";
			["pt-br"] = "Chapéus";
			["ko"] = "모자";
			["zh-tw"] = "帽子";
			["zh-cn"] = "帽子";
		}
	},
	{
		key = "HatsLandscapeTitle";
		values =
		{
			["en-us"] = "Hat";
			["es"] = "Sombrero";
			["de"] = "Hut";
			["fr"] = "Chapeau";
			["pt-br"] = "Chapéu";
			["ko"] = "모자";
			["zh-tw"] = "帽子";
			["zh-cn"] = "帽子";
		}
	},
	{
		key = "HairTitle";
		values =
		{
			["en-us"] = "Hair";
			["es"] = "Pelo";
			["de"] = "Haare";
			["fr"] = "Cheveux";
			["pt-br"] = "Cabelo";
			["ko"] = "헤어";
			["zh-tw"] = "頭髮";
			["zh-cn"] = "头发";
		}
	},
	{
		key = "FaceAccessoryTitle";
		values =
		{
			["en-us"] = "Face Accessories";
			["es"] = "Accesorios para la cara";
			["de"] = "Gesicht-Accessoires";
			["fr"] = "Accessoires de visage";
			["pt-br"] = "Acessórios de rosto";
			["ko"] = "얼굴 액세서리";
			["zh-tw"] = "臉部配件";
			["zh-cn"] = "脸部配饰";
		}
	},
	{
		key = "FaceAccessoryLandscapeTitle";
		values =
		{
			["en-us"] = "Face";
			["es"] = "Cara";
			["de"] = "Gesicht";
			["fr"] = "Visage";
			["pt-br"] = "Rosto";
			["ko"] = "얼굴";
			["zh-tw"] = "臉";
			["zh-cn"] = "脸部";
		}
	},
	{
		key = "NeckAccessoryTitle";
		values =
		{
			["en-us"] = "Neck Accessories";
			["es"] = "Accesorios para el cuello";
			["de"] = "Hals-Accessoires";
			["fr"] = "Accessoires de cou";
			["pt-br"] = "Acessórios de pescoço";
			["ko"] = "목 액세서리";
			["zh-tw"] = "頸部配件";
			["zh-cn"] = "颈部配饰";
		}
	},
	{
		key = "NeckAccessoryLandscapeTitle";
		values =
		{
			["en-us"] = "Neck";
			["es"] = "Cuello";
			["de"] = "Hals";
			["fr"] = "Cou";
			["pt-br"] = "Pescoço";
			["ko"] = "목";
			["zh-tw"] = "頸";
			["zh-cn"] = "颈部";
		}
	},
	{
		key = "ShoulderAccessoryTitle";
		values =
		{
			["en-us"] = "Shoulder Accessories";
			["es"] = "Accesorios para el hombro";
			["de"] = "Schulter-Accessoires";
			["fr"] = "Accessoires d'épaule";
			["pt-br"] = "Acessórios de ombro";
			["ko"] = "어깨 액세서리";
			["zh-tw"] = "肩膀配件";
			["zh-cn"] = "肩膀配饰";
		}
	},
	{
		key = "ShoulderAccessoryLandscapeTitle";
		values =
		{
			["en-us"] = "Shoulder";
			["es"] = "Hombro";
			["de"] = "Schulter";
			["fr"] = "Épaules";
			["pt-br"] = "Ombro";
			["ko"] = "어깨";
			["zh-tw"] = "肩";
			["zh-cn"] = "肩膀";
		}
	},
	{
		key = "FrontAccessoryTitle";
		values =
		{
			["en-us"] = "Front Accessories";
			["es"] = "Accesorios frontales";
			["de"] = "Vorderseite-Accessoires";
			["fr"] = "Accessoires avant";
			["pt-br"] = "Acessórios da frente";
			["ko"] = "가슴 액세서리";
			["zh-tw"] = "正面配件";
			["zh-cn"] = "正面配饰";
		}
	},
	{
		key = "FrontAccessoryLandscapeTitle";
		values =
		{
			["en-us"] = "Front";
			["es"] = "Frontal";
			["de"] = "Vorderseite";
			["fr"] = "Avant";
			["pt-br"] = "Frente";
			["ko"] = "가슴";
			["zh-tw"] = "正面";
			["zh-cn"] = "正面";
		}
	},
	{
		key = "BackAccessoryTitle";
		values =
		{
			["en-us"] = "Back Accessories";
			["es"] = "Accesorios traseros";
			["de"] = "Rückseite-Accessoires";
			["fr"] = "Accessoires arrière";
			["pt-br"] = "Acessórios de costas";
			["ko"] = "등 액세서리";
			["zh-tw"] = "背面配件";
			["zh-cn"] = "背面配饰";
		}
	},
	{
		key = "BackAccessoryLandscapeTitle";
		values =
		{
			["en-us"] = "Back";
			["es"] = "Trasero";
			["de"] = "Rückseite";
			["fr"] = "Retour";
			["pt-br"] = "Costas";
			["ko"] = "등";
			["zh-tw"] = "背面";
			["zh-cn"] = "背面";
		}
	},
	{
		key = "WaistAccessoryTitle";
		values =
		{
			["en-us"] = "Waist Accessories";
			["es"] = "Accesorios para la cintura";
			["de"] = "Taille-Accessoires";
			["fr"] = "Accessoires de taille";
			["pt-br"] = "Acessórios de cintura";
			["ko"] = "허리 액세서리";
			["zh-tw"] = "腰部配件";
			["zh-cn"] = "腰部配饰";
		}
	},
	{
		key = "WaistAccessoryLandscapeTitle";
		values =
		{
			["en-us"] = "Waist";
			["es"] = "Cintura";
			["de"] = "Taille";
			["fr"] = "Taille";
			["pt-br"] = "Cintura";
			["ko"] = "허리";
			["zh-tw"] = "腰";
			["zh-cn"] = "腰部";
		}
	},
	{
		key = "ShirtsTitle";
		values =
		{
			["en-us"] = "Shirts";
			["es"] = "Camisas";
			["de"] = "Hemden";
			["fr"] = "Chemises";
			["pt-br"] = "Camisas";
			["ko"] = "셔츠";
			["zh-tw"] = "上衣";
			["zh-cn"] = "衬衫";
		}
	},
	{
		key = "ShirtsLandscapeTitle";
		values =
		{
			["en-us"] = "Shirt";
			["es"] = "Camisa";
			["de"] = "Hemd";
			["fr"] = "Chemise";
			["pt-br"] = "Camisa";
			["ko"] = "셔츠";
			["zh-tw"] = "上衣";
			["zh-cn"] = "衬衫";
		}
	},
	{
		key = "PantsTitle";
		values =
		{
			["en-us"] = "Pants";
			["es"] = "Pantalones";
			["de"] = "Hosen";
			["fr"] = "Pantalons";
			["pt-br"] = "Calças";
			["ko"] = "바지";
			["zh-tw"] = "褲子";
			["zh-cn"] = "裤子";
		}
	},
	{
		key = "FacesTitle";
		values =
		{
			["en-us"] = "Faces";
			["es"] = "Caras";
			["de"] = "Gesichter";
			["fr"] = "Visages";
			["pt-br"] = "Rostos";
			["ko"] = "얼굴";
			["zh-tw"] = "臉";
			["zh-cn"] = "脸部";
		}
	},
	{
		key = "FacesLandscapeTitle";
		values =
		{
			["en-us"] = "Face";
			["es"] = "Cara";
			["de"] = "Gesicht";
			["fr"] = "Visage";
			["pt-br"] = "Rosto";
			["ko"] = "얼굴";
			["zh-tw"] = "臉";
			["zh-cn"] = "脸部";
		}
	},
	{
		key = "HeadsTitle";
		values =
		{
			["en-us"] = "Heads";
			["es"] = "Cabezas";
			["de"] = "Köpfe";
			["fr"] = "Têtes";
			["pt-br"] = "Cabeças";
			["ko"] = "머리";
			["zh-tw"] = "頭";
			["zh-cn"] = "头部";
		}
	},
	{
		key = "HeadsLandscapeTitle";
		values =
		{
			["en-us"] = "Head";
			["es"] = "Cabeza";
			["de"] = "Kopf";
			["fr"] = "Tête";
			["pt-br"] = "Cabeça";
			["ko"] = "머리";
			["zh-tw"] = "頭";
			["zh-cn"] = "头部";
		}
	},
	{
		key = "TorsosTitle";
		values =
		{
			["en-us"] = "Torsos";
			["es"] = "Torsos";
			["de"] = "Torsos";
			["fr"] = "Torses";
			["pt-br"] = "Torsos";
			["ko"] = "상체";
			["zh-tw"] = "身體";
			["zh-cn"] = "身体主干";
		}
	},
	{
		key = "TorsosLandscapeTitle";
		values =
		{
			["en-us"] = "Torso";
			["es"] = "Torso";
			["de"] = "Torso";
			["fr"] = "Torse";
			["pt-br"] = "Torso";
			["ko"] = "상체";
			["zh-tw"] = "軀幹";
			["zh-cn"] = "身体主干";
		}
	},
	{
		key = "RightArmsTitle";
		values =
		{
			["en-us"] = "Right Arms";
			["es"] = "Brazos derechos";
			["de"] = "Rechte Arme";
			["fr"] = "Bras droits";
			["pt-br"] = "Braços direitos";
			["ko"] = "오른팔";
			["zh-tw"] = "右臂";
			["zh-cn"] = "右臂";
		}
	},
	{
		key = "LeftArmsTitle";
		values =
		{
			["en-us"] = "Left Arms";
			["es"] = "Brazos izquierdos";
			["de"] = "Linke Arme";
			["fr"] = "Bras gauches";
			["pt-br"] = "Braços esquerdos";
			["ko"] = "왼팔";
			["zh-tw"] = "左臂";
			["zh-cn"] = "左臂";
		}
	},
	{
		key = "RightLegsTitle";
		values =
		{
			["en-us"] = "Right Legs";
			["es"] = "Piernas derechas";
			["de"] = "Rechte Beine";
			["fr"] = "Jambes droites";
			["pt-br"] = "Pernas direitas";
			["ko"] = "오른 다리";
			["zh-tw"] = "右腿";
			["zh-cn"] = "右腿";
		}
	},
	{
		key = "LeftLegsTitle";
		values =
		{
			["en-us"] = "Left Legs";
			["es"] = "Piernas izquierdas";
			["de"] = "Linke Beine";
			["fr"] = "Jambes gauches";
			["pt-br"] = "Pernas esquerdas";
			["ko"] = "왼 다리";
			["zh-tw"] = "左腿";
			["zh-cn"] = "左腿";
		}
	},
	{
		key = "GearTitle";
		values =
		{
			["en-us"] = "Gear";
			["es"] = "Equipamiento";
			["de"] = "Ausrüstung";
			["fr"] = "Équipement";
			["pt-br"] = "Equipamentos";
			["ko"] = "기어";
			["zh-tw"] = "裝備";
			["zh-cn"] = "装备";
		}
	},
	{
		key = "SkinToneTitle";
		values =
		{
			["en-us"] = "Skin Tone";
			["es"] = "Tono de piel";
			["de"] = "Hautfarbe";
			["fr"] = "Teint";
			["pt-br"] = "Cor de pele";
			["ko"] = "피부 색조";
			["zh-tw"] = "膚色";
			["zh-cn"] = "肤色";
		}
	},
	{
		key = "ScaleTitle";
		values =
		{
			["en-us"] = "Scale";
			["es"] = "Escala";
			["de"] = "Größe";
			["fr"] = "Taille";
			["pt-br"] = "Dimensionar";
			["ko"] = "크기";
			["zh-tw"] = "比例";
			["zh-cn"] = "大小";
		}
	},
	{
		key = "ScaleHeightTitle";
		values =
		{
			["en-us"] = "Height";
			["es"] = "Altura";
			["de"] = "Höhe";
			["fr"] = "Hauteur";
			["pt-br"] = "Altura";
			["ko"] = "높이";
			["zh-tw"] = "高度";
			["zh-cn"] = "高度";
		}
	},
	{
		key = "ScaleWidthTitle";
		values =
		{
			["en-us"] = "Width";
			["es"] = "Anchura";
			["de"] = "Breite";
			["fr"] = "Largeur";
			["pt-br"] = "Largura";
			["ko"] = "넓이";
			["zh-tw"] = "寬度";
			["zh-cn"] = "宽度";
		}
	},
	{
		key = "ScaleHeadTitle";
		values =
		{
			["en-us"] = "Head";
			["es"] = "Cabeza";
			["de"] = "Kopf";
			["fr"] = "Tête";
			["pt-br"] = "Cabeça";
			["ko"] = "머리";
			["zh-tw"] = "頭";
			["zh-cn"] = "头部";
		}
	},
	{
		key = "ScaleBodyTypeTitle";
		values =
		{
			["en-us"] = "Body Type";
			["es"] = "Tipo de cuerpo";
			["de"] = "Körpertyp";
			["fr"] = "Type de corps";
			["pt-br"] = "Tipo de corpo";
			["ko"] = "신체 유형";
			["zh-tw"] = "內文類型";
			["zh-cn"] = "体形";
		}
	},
	{
		key = "ScaleProportionTitle";
		values =
		{
			["en-us"] = "Proportions";
			["es"] = "Proporciones";
			["de"] = "Proportionen";
			["fr"] = "Proportions";
			["pt-br"] = "Proporções";
			["ko"] = "비율";
			["zh-tw"] = "比例";
			["zh-cn"] = "比例";
		}
	},
	{
		key = "ClimbAnimationsWord";
		values =
		{
			["en-us"] = "Climb Animations";
			["es"] = "Animaciones de escalada";
			["de"] = "Kletteranimationen";
			["fr"] = "Animations d'escalade";
			["pt-br"] = "Animações de escalada";
			["ko"] = "오르기 애니메이션";
			["zh-tw"] = "攀查動畫";
			["zh-cn"] = "攀爬动画";
		}
	},
	{
		key = "JumpAnimationsWord";
		values =
		{
			["en-us"] = "Jump Animations";
			["es"] = "Animaciones de salto";
			["de"] = "Springanimationen";
			["fr"] = "Animations de saut";
			["pt-br"] = "Animações de salto";
			["ko"] = "점프 애니메이션";
			["zh-tw"] = "跳躍動畫";
			["zh-cn"] = "跳跃动画";
		}
	},
	{
		key = "FallAnimationsWord";
		values =
		{
			["en-us"] = "Fall Animations";
			["es"] = "Animaciones de caída";
			["de"] = "Fallanimationen";
			["fr"] = "Animations de chute";
			["pt-br"] = "Animações de queda";
			["ko"] = "낙하 애니메이션";
			["zh-tw"] = "下降動畫";
			["zh-cn"] = "下降动画";
		}
	},
	{
		key = "IdleAnimationsWord";
		values =
		{
			["en-us"] = "Idle Animations";
			["es"] = "Animaciones de inactividad";
			["de"] = "Untätige Animationen";
			["fr"] = "Animations d'inaction";
			["pt-br"] = "Animações de inatividade";
			["ko"] = "기본 애니메이션";
			["zh-tw"] = "閒置動畫";
			["zh-cn"] = "闲置动画";
		}
	},
	{
		key = "WalkAnimationsWord";
		values =
		{
			["en-us"] = "Walk Animations";
			["es"] = "Animaciones de marcha";
			["de"] = "Gehanimationen";
			["fr"] = "Animations de marche";
			["pt-br"] = "Animações de caminhada";
			["ko"] = "걷기 애니메이션";
			["zh-tw"] = "步行動畫";
			["zh-cn"] = "行走动画";
		}
	},
	{
		key = "RunAnimationsWord";
		values =
		{
			["en-us"] = "Run Animations";
			["es"] = "Animaciones de carrera";
			["de"] = "Laufanimationen";
			["fr"] = "Animations de course";
			["pt-br"] = "Animações de corrida";
			["ko"] = "달리기 애니메이션";
			["zh-tw"] = "奔跑動畫";
			["zh-cn"] = "跑步动画";
		}
	},
	{
		key = "SwimAnimationsWord";
		values =
		{
			["en-us"] = "Swim Animations";
			["es"] = "Animaciones de nado";
			["de"] = "Schwimmanimationen";
			["fr"] = "Animations de nage";
			["pt-br"] = "Animações de nado";
			["ko"] = "수영 애니메이션";
			["zh-tw"] = "游泳動畫";
			["zh-cn"] = "游泳动画";
		}
	},
	{
		key = "ClimbWord";
		values =
		{
			["en-us"] = "Climb";
			["es"] = "Escalada";
			["de"] = "Klettern";
			["fr"] = "Escalade";
			["pt-br"] = "Escalar";
			["ko"] = "오르기";
			["zh-tw"] = "攀爬";
			["zh-cn"] = "攀爬";
		}
	},
	{
		key = "JumpWord";
		values =
		{
			["en-us"] = "Jump";
			["es"] = "Salto";
			["de"] = "Springen";
			["fr"] = "Saut";
			["pt-br"] = "Pular";
			["ko"] = "점프";
			["zh-tw"] = "跳起";
			["zh-cn"] = "跳跃";
		}
	},
	{
		key = "FallWord";
		values =
		{
			["en-us"] = "Fall";
			["es"] = "Caída";
			["de"] = "Fallen";
			["fr"] = "Chute";
			["pt-br"] = "Cair";
			["ko"] = "낙하";
			["zh-tw"] = "下降";
			["zh-cn"] = "下降";
		}
	},
	{
		key = "IdleWord";
		values =
		{
			["en-us"] = "Idle";
			["es"] = "Inactividad";
			["de"] = "Untätig";
			["fr"] = "Inaction";
			["pt-br"] = "Inatividade";
			["ko"] = "기본";
			["zh-tw"] = "閒置";
			["zh-cn"] = "闲置";
		}
	},
	{
		key = "WalkWord";
		values =
		{
			["en-us"] = "Walk";
			["es"] = "Marcha";
			["de"] = "Gehen";
			["fr"] = "Marche";
			["pt-br"] = "Andar";
			["ko"] = "걷기";
			["zh-tw"] = "步行";
			["zh-cn"] = "行走";
		}
	},
	{
		key = "RunWord";
		values =
		{
			["en-us"] = "Run";
			["es"] = "Carrera";
			["de"] = "Laufen";
			["fr"] = "Course";
			["pt-br"] = "Correr";
			["ko"] = "달리기";
			["zh-tw"] = "奔跑";
			["zh-cn"] = "跑步";
		}
	},
	{
		key = "SwimWord";
		values =
		{
			["en-us"] = "Swim";
			["es"] = "Nado";
			["de"] = "Schwimmen";
			["fr"] = "Nage";
			["pt-br"] = "Nadar";
			["ko"] = "수영";
			["zh-tw"] = "游泳";
			["zh-cn"] = "游泳";
		}
	},
	{
		key = "NoAssetsPhrase";
		values =
		{
			["en-us"] = "You don't have any %s";
			["es"] = "No tienes %s";
			["de"] = "Du hast keine %s.";
			["fr"] = "%s : rien à afficher";
			["pt-br"] = "Você não possui nenhum(a) %s";
			["ko"] = "보유한 %s이(가) 없어요.";
			["zh-tw"] = "您完全沒有%s";
			["zh-cn"] = "你没有 %s";
		}
	},
	{
		key = "RecentItemsWord";
		values =
		{
			["en-us"] = "recent items";
			["es"] = "objetos recientes";
			["de"] = "kürzlich verwendeten Gegenstände";
			["fr"] = "objets récents";
			["pt-br"] = "itens recentes";
			["ko"] = "최근 아이템";
			["zh-tw"] = "近期項目";
			["zh-cn"] = "最近项目";
		}
	},
	{
		key = "RecommendedWord";
		values =
		{
			["en-us"] = "Recommended";
			["es"] = "Recomendado";
			["de"] = "Empfohlen";
			["fr"] = "Recommandés";
			["pt-br"] = "Recomendado";
			["ko"] = "추천";
			["zh-tw"] = "推薦";
			["zh-cn"] = "推荐";
		}
	},
	{
		key = "WearWord";
		values =
		{
			["en-us"] = "Wear";
			["es"] = "Vestir";
			["de"] = "Tragen";
			["fr"] = "Porter";
			["pt-br"] = "Usar";
			["ko"] = "착용";
			["zh-tw"] = "穿戴";
			["zh-cn"] = "穿戴";
		}
	},
	{
		key = "TakeOffWord";
		values =
		{
			["en-us"] = "Take Off";
			["es"] = "Quitar";
			["de"] = "Ablegen";
			["fr"] = "Retirer";
			["pt-br"] = "Remover";
			["ko"] = "해제";
			["zh-tw"] = "取下";
			["zh-cn"] = "移去";
		}
	},
	{
		key = "CancelWord";
		values =
		{
			["en-us"] = "Cancel";
			["es"] = "Cancelar";
			["de"] = "Abbrechen";
			["fr"] = "Annuler";
			["pt-br"] = "Cancelar";
			["ko"] = "취소";
			["zh-tw"] = "取消";
			["zh-cn"] = "取消";
		}
	},
	{
		key = "ViewDetailsWord";
		values =
		{
			["en-us"] = "View details";
			["es"] = "Ver detalles";
			["de"] = "Infos anzeigen";
			["fr"] = "Voir les détails";
			["pt-br"] = "Ver detalhes";
			["ko"] = "자세히 보기";
			["zh-tw"] = "檢視詳情";
			["zh-cn"] = "查看详情";
		}
	},
	{
		key = "ScalingForR15Phrase";
		values =
		{
			["en-us"] = "Scaling only works\nfor R15 avatars";
			["es"] = "El escalado solo funciona\ncon avatares R15";
			["de"] = "Skalierung funktioniert nur\nfür R15-Avatare.";
			["fr"] = "Le changement de taille ne fonctionne\nque pour les avatars R15";
			["pt-br"] = "Dimensionamento só funciona\npara avatares R15";
			["ko"] = "크기 변경은\nR15 아바타만 가능";
			["zh-tw"] = "縮放僅適用於\nR15 虛擬人偶";
			["zh-cn"] = "缩放仅适用于\nR15 虚拟形象";
		}
	},
	{
		key = "ScalingForR15ConsolePhrase";
		values =
		{
			["en-us"] = "Scaling only works for R15 avatars";
			["es"] = "El escalado solo funciona con avatares R15";
			["de"] = "Skalierung funktioniert nur für R15-Avatare.";
			["fr"] = "Le changement de taille ne fonctionne que pour les avatars R15";
			["pt-br"] = "Dimensionamento só funciona para avatares R15";
			["ko"] = "크기 변경은 R15 아바타만 가능";
			["zh-tw"] = "縮放僅適用於 R15 虛擬人偶";
			["zh-cn"] = "缩放仅适用于 R15 虚拟形象";
		}
	},
	{
		key = "AnimationsForR15Phrase";
		values =
		{
			["en-us"] = "Animations only work\nfor R15 avatars";
			["es"] = "Las animaciones solo funcionan\ncon avatares R15";
			["de"] = "Animationen funktionieren nur\nfür R15-Avatare.";
			["fr"] = "Les animations ne fonctionnent\nque pour les avatars R15";
			["pt-br"] = "Animações só funcionam\npara avatares R15";
			["ko"] = "애니메이션은\nR15 아바타만 가능";
			["zh-tw"] = "動畫僅適用於\nR15 虛擬人偶";
			["zh-cn"] = "动画仅适用于\nR15 虚拟形象";
		}
	},
	{
		key = "AnimationsForR15ConsolePhrase";
		values =
		{
			["en-us"] = "Animations only work for R15 avatars";
			["es"] = "Las animaciones solo funcionan con avatares R15";
			["de"] = "Animationen funktionieren nur für R15-Avatare.";
			["fr"] = "Les animations ne fonctionnent que pour les avatars R15";
			["pt-br"] = "Animações só funcionam para avatares R15";
			["ko"] = "애니메이션은 R15 아바타만 가능";
			["zh-tw"] = "動畫僅適用於 R15 虛擬人偶";
			["zh-cn"] = "动画仅适用于 R15 虚拟形象";
		}
	},
	{
		key = "R15OnlyPhrase";
		values =
		{
			["en-us"] = "This feature is only available for R15";
			["es"] = "Esta función solo está disponible con R15";
		}
	},
	{
		key = "DefaultClothingAppliedPhrase";
		values =
		{
			["en-us"] = "Default clothing has been applied to your avatar - wear something from your wardrobe";
			["es"] = "Se le ha aplicado la ropa predeterminada a tu avatar. Viste algo de tu guardarropa";
			["de"] = "Dein Avatar trägt die Standardkleidung. Zieh doch etwas aus deinem Kleiderschrank an.";
			["fr"] = "Les vêtements par défaut ont été appliqués à votre avatar ; enfilez des pièces de votre garde-robe.";
			["pt-br"] = "Roupas padrão foram aplicadas ao avatar. Vista algo do seu guarda-roupa.";
			["ko"] = "기본 복장이 아바타에 적용되었어요. 옷장에서 선택하여 착용해보세요.";
			["zh-tw"] = "預設衣物已套用至您的虛擬人偶 - 請自您的衣櫃取一些衣物穿戴。";
			["zh-cn"] = "默认服装已应用至你的虚拟形象 - 从你的衣柜里挑选喜爱的搭配吧！";
		}
	},
	{
		key = "ShopNowWord";
		values =
		{
			["en-us"] = "Shop Now";
			["es"] = "Comprar";
			["de"] = "Jetzt einkaufen";
			["fr"] = "Acheter maintenant";
			["pt-br"] = "Comprar agora";
			["ko"] = "지금 구매";
			["zh-tw"] = "立即選購";
			["zh-cn"] = "立即购买";
		}
	},
})

function this:GetLocale()
	if LoadAvatarEditorTranslations then
		return game:GetService("LocalizationService").RobloxLocaleId
	end
	return "en-us"
end

function this:GetAvatarEditorString(locale, stringKey)
	local success, result = pcall(function()
		return AvatarEditorStringsTable:GetString(locale, stringKey)
	end)

	if success and result then
		return result
	end

	return nil
end

function this:LocalizedString(stringKey)
	local locale = self:GetLocale()
	local localeLanguage = locale and string.sub(locale, 1, 2)
	local result = locale and self:GetAvatarEditorString(locale, stringKey) or
		self:GetAvatarEditorString(localeLanguage, stringKey)
	if not result then
		if UserSettings().GameSettings:InStudioMode() then
			print("LocalizedString: Could not find string for:" , stringKey , "using locale:" , locale)
		end
		result = self:GetAvatarEditorString("en-us", stringKey) or stringKey
	end
	return result
end

return this
