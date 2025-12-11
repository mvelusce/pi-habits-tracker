# Calendar View Feature

## Overview

The Calendar View provides a comprehensive monthly view of all your lifestyle factors, making it easy to track your habits over time and see patterns at a glance.

## Features

### 📅 Monthly Calendar Display
- **Full Month View**: See an entire month of your lifestyle factor tracking at once
- **Visual Completion Indicators**: Color-coded cells show your daily completion rate:
  - **Green** (67-100%): Excellent progress! 🌟
  - **Yellow** (34-66%): Good progress! 💪
  - **Red** (0-33%): Room for improvement 🌱
  - **White**: No entries yet

### 🎯 Easy Navigation
- **Month Navigation**: Use left/right arrows to browse through months
- **Today Button**: Quickly jump back to the current month
- **Today Highlight**: Current day is highlighted with a blue ring

### 🔍 Category Filtering
- **Filter Button**: Click the filter icon to show/hide category filter
- **Multi-Category Support**: Filter by specific categories (Health, Fitness, Nutrition, etc.)
- **Show All**: View all lifestyle factors across all categories

### ✅ Day Detail Modal
Click on any day to:
- **View All Factors**: See all lifestyle factors for that specific day
- **Quick Toggle**: Mark factors as complete/incomplete with a single click
- **Visual Feedback**: Completed items are shown with checkmarks and strikethrough
- **Category Labels**: Each factor displays its category
- **Color Coding**: Factors display with their custom color and icon

### 📊 At-a-Glance Stats
Each calendar day shows:
- **Completion Count**: X/Y format showing completed vs total factors
- **Emoji Indicator**: Visual feedback based on progress:
  - 🌟 = 100% complete
  - 🔥 = 67%+ complete
  - 💪 = 34%+ complete
  - 🌱 = 1-33% complete

## How to Use

### Accessing the Calendar View
1. Click on the **Calendar** icon in the bottom navigation bar
2. Or navigate to `/calendar` in your browser

### Viewing a Specific Day
1. Click on any day in the current month (greyed-out days from other months are not clickable)
2. A modal will open showing all lifestyle factors for that day
3. Toggle factors on/off as needed
4. Close the modal by clicking the "Close" button or the X icon

### Filtering by Category
1. Click the **Filter** icon (funnel symbol) in the top right
2. Select a category to view only factors from that category
3. The calendar will update to show only filtered factors
4. Click "All" to view all categories again
5. Hide the filter panel by clicking the X icon or filter icon again

### Navigating Months
1. Use the **left arrow (←)** to view previous months
2. Use the **right arrow (→)** to view future months
3. Click **Today** to return to the current month

## Technical Details

### Component Location
- Main Component: `/frontend/src/components/LifestyleFactorCalendar.tsx`
- Page Component: `/frontend/src/pages/Calendar.tsx`
- Route: `/calendar`

### Data Loading
- The calendar loads lifestyle factors and entries for the current month ± 1 week
- Data is fetched when:
  - The component first loads
  - The month changes
  - After toggling a factor

### Performance
- Efficiently loads only the necessary date range
- Local state updates for instant UI feedback
- Optimistic updates with server sync

## Design Considerations

### Mobile-Friendly
- Responsive grid layout
- Touch-friendly buttons and modals
- Scrollable day detail modal for many factors

### Accessibility
- Semantic HTML structure
- Color coding supplemented with text and emoji indicators
- Keyboard navigable (modal close on Esc)

### User Experience
- **Visual Hierarchy**: Important information is prominently displayed
- **Consistent Colors**: Uses the same color scheme as other views
- **Immediate Feedback**: Toggle actions show toast notifications
- **Error Handling**: Graceful error messages if loading fails

## Future Enhancements (Ideas)

Some potential improvements for the future:
- **Week View**: Alternative view showing one week at a time with more detail
- **Year Overview**: Bird's-eye view of the entire year
- **Streak Indicators**: Show current streaks on the calendar
- **Notes on Calendar**: Display notes icon when a day has notes
- **Bulk Actions**: Select multiple days to update at once
- **Export Calendar**: Export calendar view as image or PDF
- **Custom Date Range**: Select specific date ranges to view

## API Endpoints Used

- `GET /api/lifestyle-factors` - Fetch all active lifestyle factors
- `GET /api/lifestyle-factors/entries/range` - Fetch entries for date range
- `POST /api/lifestyle-factors/entries` - Create/update entry
- `GET /api/lifestyle-factors/categories/list` - Fetch available categories

